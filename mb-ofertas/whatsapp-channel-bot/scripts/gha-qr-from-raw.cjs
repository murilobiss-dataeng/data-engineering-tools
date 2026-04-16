/**
 * Empacota o QR já gerado pelo bot (data/qr-url.txt = data URL PNG).
 * NÃO re-gera QR a partir do raw com outras opções — isso podia divergir e falhar no scan.
 * Fallback: só se não existir qr-url.txt, gera com as mesmas opções do src/index.js.
 */
const fs = require("fs");
const path = require("path");
const QRCode = require("qrcode");

/** Deve coincidir com QR_IMAGE_OPTS em src/index.js */
const QR_IMAGE_OPTS = {
  margin: 4,
  width: 768,
  errorCorrectionLevel: "M",
};

const root = process.env.GITHUB_WORKSPACE;
const dataDir = path.join(process.cwd(), "data");
const urlPath = path.join(dataDir, "qr-url.txt");
const rawPath = path.join(dataDir, "qr-raw.txt");
const pngFromBot = path.join(dataDir, "qr.png");

function writeWorkflowFiles(dataUrl, label) {
  if (!root) {
    console.error("gha-qr-from-raw: GITHUB_WORKSPACE não definido.");
    process.exit(1);
  }
  const m = /^data:image\/png;base64,(.+)$/i.exec(dataUrl.trim());
  if (!m) {
    console.error("gha-qr-from-raw: data URL PNG inválida.");
    process.exit(1);
  }
  const buf = Buffer.from(m[1], "base64");
  const outPng = path.join(root, "qr-workflow.png");
  fs.writeFileSync(outPng, buf);
  const outHtml = path.join(root, "qr-workflow.html");
  const body =
    `<!DOCTYPE html><html><head><meta charset="utf-8"><title>QR WhatsApp</title></head>` +
    `<body style="margin:20px;font-family:sans-serif"><h2>QR (mesmo PNG do bot)</h2>` +
    `<p style="color:#444;font-size:14px">${label}</p>` +
    `<img style="image-rendering:pixelated;image-rendering:crisp-edges;max-width:min(98vw,768px);height:auto" src="${dataUrl}" width="768" height="768" alt="QR"/></body></html>`;
  fs.writeFileSync(outHtml, body, "utf8");
  console.log("gha-qr-from-raw: qr-workflow.png/html a partir de", label);
}

(async () => {
  try {
    if (fs.existsSync(urlPath)) {
      const dataUrl = fs.readFileSync(urlPath, "utf8").trim();
      if (dataUrl.startsWith("data:image/png;base64,")) {
        writeWorkflowFiles(dataUrl, "data/qr-url.txt");
        process.exit(0);
      }
    }
    if (fs.existsSync(pngFromBot)) {
      const buf = fs.readFileSync(pngFromBot);
      const b64 = buf.toString("base64");
      const dataUrl = `data:image/png;base64,${b64}`;
      writeWorkflowFiles(dataUrl, "data/qr.png");
      process.exit(0);
    }
    if (!fs.existsSync(rawPath)) {
      console.log("gha-qr-from-raw: sem qr-url.txt / qr.png / qr-raw.txt; pulando.");
      process.exit(0);
    }
    const raw = fs.readFileSync(rawPath, "utf8").trim();
    if (!raw) {
      console.log("gha-qr-from-raw: qr-raw.txt vazio; pulando.");
      process.exit(0);
    }
    console.log(
      "::warning::Sem qr-url.txt; gerando fallback a partir de qr-raw.txt (ideal: usar só o QR do bot)."
    );
    const dataUrl = await QRCode.toDataURL(raw, QR_IMAGE_OPTS);
    writeWorkflowFiles(dataUrl, "fallback QRCode.toDataURL(qr-raw)");
    process.exit(0);
  } catch (e) {
    console.error("gha-qr-from-raw:", e && e.message ? e.message : e);
    process.exit(1);
  }
})();
