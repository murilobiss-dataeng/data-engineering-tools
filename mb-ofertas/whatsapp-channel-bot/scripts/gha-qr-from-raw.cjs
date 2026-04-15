/**
 * Adicional ao fluxo principal (qr-url.txt → qr.html): lê data/qr-raw.txt,
 * gera PNG data URL com a mesma lib `qrcode` e grava qr-workflow.html + Summary.
 */
const fs = require("fs");
const path = require("path");
const QRCode = require("qrcode");

const root = process.env.GITHUB_WORKSPACE;
const rawPath = path.join(process.cwd(), "data", "qr-raw.txt");

if (!fs.existsSync(rawPath)) {
  console.log("gha-qr-from-raw: sem data/qr-raw.txt; pulando geração adicional.");
  process.exit(0);
}

const raw = fs.readFileSync(rawPath, "utf8").trim();
if (!raw) {
  console.log("gha-qr-from-raw: qr-raw.txt vazio; pulando.");
  process.exit(0);
}

(async () => {
  try {
    const dataUrl = await QRCode.toDataURL(raw, { margin: 2, width: 280 });
    if (!root) {
      console.error("gha-qr-from-raw: GITHUB_WORKSPACE não definido.");
      process.exit(1);
    }
    const outHtml = path.join(root, "qr-workflow.html");
    const body = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>QR WhatsApp (workflow)</title></head><body style="margin:20px;font-family:sans-serif"><h2>QR gerado no workflow (payload bruto)</h2><img src="${dataUrl}" width="280" alt="QR"/></body></html>`;
    fs.writeFileSync(outHtml, body, "utf8");
    const summary = process.env.GITHUB_STEP_SUMMARY;
    if (summary) {
      fs.appendFileSync(
        summary,
        "\n---\n\n## QR adicional (gerado no workflow a partir de `data/qr-raw.txt`)\n\n" +
          `![QR workflow — mesmo scan que o QR principal](${dataUrl})\n`
      );
    }
    console.log("gha-qr-from-raw: qr-workflow.html e trecho no Summary OK.");
    process.exit(0);
  } catch (e) {
    console.error("gha-qr-from-raw:", e && e.message ? e.message : e);
    process.exit(1);
  }
})();
