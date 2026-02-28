import { Router } from "express";
import * as productsRepo from "../../repositories/products.repository.js";
import * as categoriesRepo from "../../repositories/categories.repository.js";
import { captureAmazonDeals } from "../../services/products/amazon.service.js";
import { scrapeProductFromUrl } from "../../services/products/scrape-url.service.js";
import { runFetchOfertas } from "../../services/products/fetch-ofertas.service.js";
import { inferCategorySlugFromTitle } from "../../services/products/categorize.service.js";
import { generateOfferMessage, generatePostContent } from "../../services/messages/copy-generator.js";
import type { ProductInput } from "../../services/products/types.js";

export const productsRouter = Router();

productsRouter.get("/", async (req, res) => {
  try {
    const status = req.query.status as string | undefined;
    const categoryId = req.query.categoryId as string | undefined;
    const limit = Math.min(Number(req.query.limit) || 50, 100);
    const offset = Number(req.query.offset) || 0;
    const rows = await productsRepo.listProducts({ status, categoryId, limit, offset });
    res.json({ products: rows });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Busca ofertas automaticamente (Amazon + ML) — acionado pela UI ou por integração. */
productsRouter.post("/fetch-ofertas", async (req, res) => {
  try {
    const body = (req.body || {}) as { urls?: string[] };
    const result = await runFetchOfertas({
      urls: body.urls?.length ? body.urls : undefined,
      maxPerListing: 8,
      delayMs: 1500,
    });
    res.json({
      inserted: result.inserted,
      failed: result.failed,
      totalUrls: result.totalUrls,
      message:
        result.totalUrls === 0
          ? "Nenhuma URL configurada. Configure em backend/scripts/ofertas-urls.json ou OFERTAS_URLS no .env."
          : `${result.inserted} produto(s) adicionado(s) como pendentes.`,
    });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.get("/:id", async (req, res) => {
  try {
    const row = await productsRepo.getProductById(req.params.id);
    if (!row) return res.status(404).json({ error: "Produto não encontrado" });
    res.json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.patch("/:id/status", async (req, res) => {
  try {
    const { status } = req.body as { status?: string };
    if (!status || !["approved", "rejected", "sent"].includes(status)) {
      return res.status(400).json({ error: "status deve ser approved, rejected ou sent" });
    }
    await productsRepo.updateProductStatus(req.params.id, status as "approved" | "rejected" | "sent");
    const row = await productsRepo.getProductById(req.params.id);
    res.json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Atualiza a categoria do produto (para segmentação por canal). */
productsRouter.patch("/:id/category", async (req, res) => {
  try {
    const { categoryId } = req.body as { categoryId?: string | null };
    const updated = await productsRepo.updateProductCategory(req.params.id, categoryId ?? null);
    if (!updated) return res.status(404).json({ error: "Produto não encontrado" });
    const row = await productsRepo.getProductById(req.params.id);
    res.json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Reprovar = remover o produto do banco (apagar a linha). */
productsRouter.delete("/:id", async (req, res) => {
  try {
    const deleted = await productsRepo.deleteProduct(req.params.id);
    if (!deleted) return res.status(404).json({ error: "Produto não encontrado" });
    res.json({ deleted: true });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.post("/capture", async (req, res) => {
  try {
    const categorySlug = req.body?.categorySlug as string | undefined;
    const result = await captureAmazonDeals(categorySlug);
    const ids: string[] = [];
    for (const p of result.products) {
      const id = await productsRepo.insertProduct({ ...p, categoryId: req.body?.categoryId });
      ids.push(id);
    }
    res.json({ captured: result.total, inserted: ids.length, productIds: ids });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.post("/", async (req, res) => {
  try {
    const body = req.body as Partial<ProductInput> & { categoryId?: string };
    if (!body.title || body.price == null || !body.affiliateLink) {
      return res.status(400).json({ error: "title, price e affiliateLink são obrigatórios" });
    }
    let categoryId = body.categoryId ?? null;
    if (!categoryId && body.title) {
      const slug = inferCategorySlugFromTitle(body.title, { discountPct: body.discountPct });
      const cat = await categoriesRepo.getCategoryBySlug(slug);
      if (cat) categoryId = cat.id;
    }
    const id = await productsRepo.insertProduct({
      title: body.title,
      price: Number(body.price),
      previousPrice: body.previousPrice != null ? Number(body.previousPrice) : null,
      discountPct: body.discountPct != null ? Number(body.discountPct) : null,
      affiliateLink: body.affiliateLink,
      imageUrl: body.imageUrl ?? null,
      installments: body.installments ?? null,
      externalId: body.externalId,
      source: body.source ?? "manual",
      categoryId,
    });
    const row = await productsRepo.getProductById(id);
    res.status(201).json(row);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.get("/:id/preview-message", async (_req, res) => {
  try {
    const row = await productsRepo.getProductById(_req.params.id);
    if (!row) return res.status(404).json({ error: "Produto não encontrado" });
    const product: ProductInput = {
      title: row.title,
      price: parseFloat(row.price),
      previousPrice: row.previous_price ? parseFloat(row.previous_price) : null,
      discountPct: row.discount_pct ? parseFloat(row.discount_pct) : null,
      affiliateLink: row.affiliate_link,
      imageUrl: row.image_url,
      installments: row.installments ?? undefined,
    };
    const message = generateOfferMessage(product);
    res.json({ message });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Conteúdo para post: texto + URL da imagem. Query: coupon (opcional). */
productsRouter.get("/:id/post-content", async (req, res) => {
  try {
    const row = await productsRepo.getProductById(req.params.id);
    if (!row) return res.status(404).json({ error: "Produto não encontrado" });
    const product: ProductInput = {
      title: row.title,
      price: parseFloat(row.price),
      previousPrice: row.previous_price ? parseFloat(row.previous_price) : null,
      discountPct: row.discount_pct ? parseFloat(row.discount_pct) : null,
      affiliateLink: row.affiliate_link,
      imageUrl: row.image_url,
      installments: row.installments ?? undefined,
    };
    const coupon = (req.query.coupon as string)?.trim() || undefined;
    const { text, imageUrl } = generatePostContent(product, { coupon });
    res.json({ text, imageUrl });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Busca oferta a partir de URL (ex.: Amazon). Sem API oficial; scraping. */
productsRouter.post("/from-url", async (req, res) => {
  try {
    const { url } = req.body as { url?: string };
    if (!url || typeof url !== "string" || !url.trim()) {
      return res.status(400).json({ error: "Envie a URL do produto (campo url)." });
    }
    const scraped = await scrapeProductFromUrl(url.trim());
    res.json(scraped);
  } catch (err) {
    res.status(400).json({ error: (err as Error).message });
  }
});

/** Gera conteúdo para post (texto + imagem). Body: coupon (opcional), installments (opcional). */
productsRouter.post("/post-content", async (req, res) => {
  try {
    const b = req.body as {
      title?: string;
      price?: number;
      previousPrice?: number | null;
      discountPct?: number | null;
      affiliateLink?: string;
      imageUrl?: string | null;
      installments?: string | null;
      coupon?: string | null;
    };
    if (!b.title || b.price == null || !b.affiliateLink) {
      return res.status(400).json({ error: "title, price e affiliateLink são obrigatórios." });
    }
    const product: ProductInput = {
      title: b.title,
      price: Number(b.price),
      previousPrice: b.previousPrice != null ? Number(b.previousPrice) : null,
      discountPct: b.discountPct != null ? Number(b.discountPct) : null,
      affiliateLink: b.affiliateLink,
      imageUrl: b.imageUrl ?? null,
      installments: b.installments ?? undefined,
    };
    const coupon = b.coupon?.trim() || undefined;
    const { text, imageUrl } = generatePostContent(product, { coupon });
    res.json({ text, imageUrl });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
