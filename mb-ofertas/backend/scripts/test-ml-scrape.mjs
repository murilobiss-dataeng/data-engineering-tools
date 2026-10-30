import { getHtmlWithBrowser } from "../dist/services/products/browser-scraper.service.js";

const url =
  "https://www.mercadolivre.com.br/celular-samsung-galaxy-a07-256gb-8gb-cmera-50mp-tela-67-proteco-ip54-processador-6nm-preto/p/MLB54961556";

const html = await getHtmlWithBrowser(url);
console.log("len", html.length);
console.log("verification", /account-verification/i.test(html));
console.log(
  "meta price",
  html.match(/product:price:amount[^>]+content="([^"]+)"/)?.[1]
);
const fracs = [...html.matchAll(/andes-money-amount__fraction[^>]*>([^<]+)</g)]
  .slice(0, 5)
  .map((m) => m[1]);
console.log("fractions", fracs);
