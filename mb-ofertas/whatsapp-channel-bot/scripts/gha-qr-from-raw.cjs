/**
 * Adicional ao fluxo principal (qr-url.txt → qr.html): lê data/qr-raw.txt,
 * gera QR adicional no workflow (ASCII no log + PNG + HTML + Summary).
 */
const fs = require("fs");
const path = require("path");
const QRCode = require("qrcode");
const qrcodeTerminal = require("qrcode-terminal");

/** Mesmo critério do bot: payload longo precisa de módulos grandes + ECC alto. */
const QR_OPTS = { margin: 4, width: 720, errorCorrectionLevel: "H" };

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
    // 1) Mostra o QR direto no log (ASCII). Ajuda quando o render do markdown/HTML falha.
    console.log("");
    console.log("=== QR (ASCII) gerado no workflow — escaneie daqui se quiser ===");
    qrcodeTerminal.generate(raw, { small: true });
    console.log("=== fim do QR (ASCII) ===");
    console.log("");

    // 2) Gera data URL e arquivos adicionais
    const dataUrl = await QRCode.toDataURL(raw, QR_OPTS);
    if (!root) {
      console.error("gha-qr-from-raw: GITHUB_WORKSPACE não definido.");
      process.exit(1);
    }
    const outHtml = path.join(root, "qr-workflow.html");
    const outPng = path.join(root, "qr-workflow.png");
    const body = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>QR WhatsApp (workflow)</title></head><body style="margin:20px;font-family:sans-serif"><h2>QR gerado no workflow (payload bruto)</h2><img style="image-rendering:pixelated;image-rendering:crisp-edges" src="${dataUrl}" width="720" height="720" alt="QR"/></body></html>`;
    fs.writeFileSync(outHtml, body, "utf8");
    await QRCode.toFile(outPng, raw, { ...QR_OPTS, width: 1024 });

    const summary = process.env.GITHUB_STEP_SUMMARY;
    if (summary) {
      fs.appendFileSync(
        summary,
        "\n---\n\n## QR adicional (gerado no workflow a partir de `data/qr-raw.txt`)\n\n" +
          `![QR workflow — mesmo scan que o QR principal](${dataUrl})\n`
      );
    }
    console.log("gha-qr-from-raw: qr-workflow.html, qr-workflow.png e trecho no Summary OK.");
    process.exit(0);
  } catch (e) {
    console.error("gha-qr-from-raw:", e && e.message ? e.message : e);
    process.exit(1);
  }
})();
