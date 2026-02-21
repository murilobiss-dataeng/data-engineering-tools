import { Router } from "express";
import * as productsRepo from "../../repositories/products.repository.js";
import { captureAmazonDeals } from "../../services/products/amazon.service.js";
import { generateOfferMessage } from "../../services/messages/copy-generator.js";
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
    const id = await productsRepo.insertProduct({
      title: body.title,
      price: Number(body.price),
      previousPrice: body.previousPrice != null ? Number(body.previousPrice) : null,
      discountPct: body.discountPct != null ? Number(body.discountPct) : null,
      affiliateLink: body.affiliateLink,
      imageUrl: body.imageUrl ?? null,
      externalId: body.externalId,
      source: body.source ?? "manual",
      categoryId: body.categoryId,
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
    };
    const message = generateOfferMessage(product);
    res.json({ message });
  } catch (err) {
    res.status(500).json({ error: (err as Error).message });
  }
});
