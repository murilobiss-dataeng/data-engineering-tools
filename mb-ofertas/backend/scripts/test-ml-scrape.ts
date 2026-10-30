import * as cheerio from "cheerio";
import { getHtmlWithBrowser } from "../src/services/products/browser-scraper.service.js";

async function test(url: string, label: string) {
  console.log("\n===", label, "===");
  const html = await getHtmlWithBrowser(url);
  console.log("len", html.length);
  console.log("verification", /account-verification/i.test(html));
  const $ = cheerio.load(html);
  console.log(
    "meta price",
    $('meta[property="product:price:amount"]').attr("content")
  );
  console.log("title", $(".ui-pdp-title").first().text().trim().slice(0, 80));
  const cards = $('[class*="poly-card"], .ui-search-layout__item, [data-testid="item"]');
  console.log("cards", cards.length);
  cards.slice(0, 3).each((i, el) => {
    const card = $(el);
    const href = card.find('a[href*="/p/MLB"], a[href*="MLB"]').first().attr("href");
    const price = card.find(".andes-money-amount__fraction").first().text().trim();
    const title = card
      .find(".poly-component__title, h2, [class*='title']")
      .first()
      .text()
      .trim()
      .slice(0, 60);
    console.log({ i, href: href?.slice(0, 80), price, title });
  });
}

async function main() {
  await test(
    "https://www.mercadolivre.com.br/ofertas",
    "ofertas listing"
  );
  await test(
    "https://www.mercadolivre.com.br/celular-samsung-galaxy-a07-256gb-8gb-cmera-50mp-tela-67-proteco-ip54-processador-6nm-preto/p/MLB54961556",
    "product page"
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
