import { Router } from "express";
import * as productsRepo from "../../repositories/products.repository.js";
import * as categoriesRepo from "../../repositories/categories.repository.js";
import * as shortLinksRepo from "../../repositories/short-links.repository.js";
import { captureAmazonDeals } from "../../services/products/amazon.service.js";
import { scrapeProductFromUrlWithFallback } from "../../services/products/scrape-url.service.js";
import { runFetchOfertas } from "../../services/products/fetch-ofertas.service.js";
import { inferCategorySlugFromTitle } from "../../services/products/categorize.service.js";
import { generateOfferMessage, generatePostContent } from "../../services/messages/copy-generator.js";
import { toTwoDecimalsString } from "../../utils/price.js";
import { parseInstallmentParts } from "../../utils/installments.js";
import type { ProductInput } from "../../services/products/types.js";

/** Formata preços do row para sempre 2 casas decimais (ex.: 386.1 → "386.10"). */
function formatProductRow<
  T extends { price?: unknown; previous_price?: unknown; discount_pct?: unknown; installment_unit_price?: unknown },
>(row: T): T {
  return {
    ...row,
    price: toTwoDecimalsString(row.price as number | string) ?? row.price,
    previous_price: row.previous_price != null ? (toTwoDecimalsString(row.previous_price as number | string) ?? row.previous_price) : null,
    discount_pct: row.discount_pct != null ? (toTwoDecimalsString(row.discount_pct as number | string) ?? row.discount_pct) : null,
    installment_unit_price:
      row.installment_unit_price != null
        ? (toTwoDecimalsString(row.installment_unit_price as number | string) ?? row.installment_unit_price)
        : null,
  };
}

/** Garante price = preço novo (menor), previousPrice = preço cheio (maior) para exibição e copy. */
function normalizeProductPrices(p: ProductInput): ProductInput {
  const prev = p.previousPrice ?? null;
  const curr = p.price;
  if (prev != null && prev > 0 && curr > 0 && prev < curr) {
    return {
      ...p,
      price: prev,
      previousPrice: curr,
      discountPct: Math.round(((curr - prev) / curr) * 100),
    };
  }
  return p;
}

function dbRowToProductInput(row: Record<string, unknown>): ProductInput {
  const installments = row.installments != null ? String(row.installments) : null;
  return normalizeProductPrices({
    title: String(row.title ?? ""),
    price: parseFloat(String(row.price)),
    previousPrice: row.previous_price != null ? parseFloat(String(row.previous_price)) : null,
    discountPct: row.discount_pct != null ? parseFloat(String(row.discount_pct)) : null,
    affiliateLink: String(row.affiliate_link ?? ""),
    imageUrl: row.image_url != null ? String(row.image_url) : null,
    installments: installments || null,
    installmentMaxTimes:
      row.installment_max_times != null && String(row.installment_max_times).trim() !== ""
        ? Number(row.installment_max_times)
        : null,
    installmentUnitPrice:
      row.installment_unit_price != null ? parseFloat(String(row.installment_unit_price)) : null,
  });
}

export const productsRouter = Router();

productsRouter.get("/", async (req, res) => {
  try {
    const status = req.query.status as string | undefined;
    const categoryId = req.query.categoryId as string | undefined;
    const limit = Math.min(Number(req.query.limit) || 50, 100);
    const offset = Number(req.query.offset) || 0;
    const rows = await productsRepo.listProducts({ status, categoryId, limit, offset });
    res.json({ products: rows.map(formatProductRow) });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/**
 * Feed para o bot WhatsApp (whatsapp-channel-bot): retorna produtos aprovados no formato
 * [{ title, text, url, imageUrl }]. O bot usa API_URL apontando para a base da API (ex. https://sua-api.onrender.com)
 * com path /api/products/feed.
 */
productsRouter.get("/feed", async (req, res) => {
  try {
    const limit = Math.min(Number(req.query.limit) || 50, 100);
    const rawSlug = (req.query.channelSlug || req.query.categorySlug || "") as string;
    const channelSlug = String(rawSlug).trim() || null;
    const rows = await productsRepo.getApprovedProducts(limit, channelSlug);
    // Só incluir produtos com imagem (essencial para engajamento no canal)
    const withImage = rows.filter((p) => p.image_url && p.image_url.trim() !== "");
    const feed = withImage.map((p) => {
      const text = generateOfferMessage(dbRowToProductInput(p));
      const slug = p.category_slug && String(p.category_slug).trim() ? String(p.category_slug).trim() : undefined;
      return {
        id: p.id,
        title: p.title,
        text,
        url: p.affiliate_link,
        imageUrl: p.image_url ?? undefined,
        ...(slug ? { channelSlug: slug, categorySlug: slug } : {}),
      };
    });
    res.setHeader("Cache-Control", "public, max-age=60");
    res.json(feed);
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/**
 * Marca produto como postado (status = 'sent'). Chamado pelo bot após enviar ao canal.
 * Body: { id?: string, url?: string }. Preferir id (vem no feed); url é fallback (affiliate_link).
 */
productsRouter.post("/feed/mark-posted", async (req, res) => {
  try {
    const body = (req.body || {}) as { id?: string; url?: string };
    let productId: string | null = null;
    if (body.id && String(body.id).trim()) {
      const row = await productsRepo.getProductById(String(body.id).trim());
      if (row) productId = row.id;
    }
    if (!productId && body.url && String(body.url).trim()) {
      productId = await productsRepo.findProductIdByAffiliateLink(String(body.url).trim());
    }
    if (!productId) return res.status(404).json({ error: "Produto não encontrado" });
    await productsRepo.updateProductStatus(productId, "sent");
    res.json({ ok: true, id: productId });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

/** Busca ofertas automaticamente (Amazon via proxy opcional + ML + Shopee API) — acionado pela UI ou por integração. */
productsRouter.post("/fetch-ofertas", async (req, res) => {
  try {
    const body = (req.body || {}) as { urls?: string[] };
    const result = await runFetchOfertas({
      urls: body.urls?.length ? body.urls : undefined,
      maxPerListing: 100,
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
    res.json(formatProductRow(row));
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.patch("/:id/status", async (req, res) => {
  try {
    const body = req.body && typeof req.body === "object" ? req.body : {};
    const status = body.status;
    if (!status || !["approved", "rejected", "sent"].includes(String(status))) {
      return res.status(400).json({ error: "status deve ser approved, rejected ou sent" });
    }
    const id = (req.params.id && String(req.params.id).trim()) || "";
    if (!id) return res.status(400).json({ error: "id é obrigatório" });
    const existing = await productsRepo.getProductById(id);
    if (!existing) return res.status(404).json({ error: "Produto não encontrado" });
    await productsRepo.updateProductStatus(id, status as "approved" | "rejected" | "sent");
    const row = await productsRepo.getProductById(id);
    if (!row) return res.status(404).json({ error: "Produto não encontrado" });
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.json(formatProductRow(row));
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    res.status(500).json({ error: msg });
  }
});

/** Atualiza a categoria do produto (para segmentação por canal). */
productsRouter.patch("/:id/category", async (req, res) => {
  try {
    const { categoryId } = req.body as { categoryId?: string | null };
    const updated = await productsRepo.updateProductCategory(req.params.id, categoryId ?? null);
    if (!updated) return res.status(404).json({ error: "Produto não encontrado" });
    const row = await productsRepo.getProductById(req.params.id);
    res.json(formatProductRow(row));
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
      const { id } = await productsRepo.insertProduct({ ...p, categoryId: req.body?.categoryId });
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
    let instMax =
      body.installmentMaxTimes != null && Number(body.installmentMaxTimes) > 0
        ? Math.floor(Number(body.installmentMaxTimes))
        : null;
    let instUnit =
      body.installmentUnitPrice != null && Number(body.installmentUnitPrice) > 0
        ? Number(body.installmentUnitPrice)
        : null;
    if ((instMax == null || instUnit == null) && body.installments) {
      const parsed = parseInstallmentParts(body.installments);
      if (parsed.maxTimes && parsed.unitPrice) {
        instMax = parsed.maxTimes;
        instUnit = parsed.unitPrice;
      }
    }
    const { id } = await productsRepo.insertProduct({
      title: body.title,
      price: Number(body.price),
      previousPrice: body.previousPrice != null ? Number(body.previousPrice) : null,
      discountPct: body.discountPct != null ? Number(body.discountPct) : null,
      affiliateLink: body.affiliateLink,
      imageUrl: body.imageUrl ?? null,
      installments: body.installments ?? null,
      installmentMaxTimes: instMax,
      installmentUnitPrice: instUnit,
      externalId: body.externalId,
      source: body.source ?? "manual",
      categoryId,
    });
    const row = await productsRepo.getProductById(id);
    res.status(201).json(formatProductRow(row));
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});

productsRouter.get("/:id/preview-message", async (req, res) => {
  try {
    const row = await productsRepo.getProductById(req.params.id);
    if (!row) return res.status(404).json({ error: "Produto não encontrado" });
    const product = dbRowToProductInput(row);
    const shortLinkBase = (req.get("X-Short-Link-Base") || req.get("x-short-link-base") || "").trim() || undefined;
    const short = await shortLinksRepo.createShortLink(row.affiliate_link, shortLinkBase, row.id);
    const message = generateOfferMessage(product, { shortLink: short.shortUrl });
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
    const product = dbRowToProductInput(row);
    const shortLinkBase = (req.get("X-Short-Link-Base") || req.get("x-short-link-base") || "").trim() || undefined;
    const short = await shortLinksRepo.createShortLink(row.affiliate_link, shortLinkBase, row.id);
    const coupon = (req.query.coupon as string)?.trim() || undefined;
    const { text, imageUrl } = generatePostContent(product, { coupon, shortLink: short.shortUrl });
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
    const scraped = await scrapeProductFromUrlWithFallback(url.trim());
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
      installmentMaxTimes?: number | null;
      installmentUnitPrice?: number | null;
      coupon?: string | null;
      /** Opcional: vínculo do link curto ao produto (analytics). */
      productId?: string | null;
    };
    if (!b.title || b.price == null || !b.affiliateLink) {
      return res.status(400).json({ error: "title, price e affiliateLink são obrigatórios." });
    }
    let instMax =
      b.installmentMaxTimes != null && Number(b.installmentMaxTimes) > 0
        ? Math.floor(Number(b.installmentMaxTimes))
        : null;
    let instUnit =
      b.installmentUnitPrice != null && Number(b.installmentUnitPrice) > 0
        ? Number(b.installmentUnitPrice)
        : null;
    if ((instMax == null || instUnit == null) && b.installments) {
      const parsed = parseInstallmentParts(b.installments);
      if (parsed.maxTimes && parsed.unitPrice) {
        instMax = parsed.maxTimes;
        instUnit = parsed.unitPrice;
      }
    }
    let product: ProductInput = {
      title: b.title,
      price: Number(b.price),
      previousPrice: b.previousPrice != null ? Number(b.previousPrice) : null,
      discountPct: b.discountPct != null ? Number(b.discountPct) : null,
      affiliateLink: b.affiliateLink,
      imageUrl: b.imageUrl ?? null,
      installments: b.installments ?? undefined,
      installmentMaxTimes: instMax,
      installmentUnitPrice: instUnit,
    };
    product = normalizeProductPrices(product);
    const shortLinkBase = (req.get("X-Short-Link-Base") || req.get("x-short-link-base") || "").trim() || undefined;
    const pid = typeof b.productId === "string" && b.productId.trim() ? b.productId.trim() : null;
    const short = await shortLinksRepo.createShortLink(b.affiliateLink, shortLinkBase, pid);
    const coupon = b.coupon?.trim() || undefined;
    const { text, imageUrl } = generatePostContent(product, { coupon, shortLink: short.shortUrl });
    res.json({ text, imageUrl });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
