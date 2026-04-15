/**
 * Usado só no GitHub Actions (Init WhatsApp): publica qr.html como artifact
 * imediatamente, sem esperar o fim do scan (o step principal continua em loop).
 */
const fs = require("fs");
const path = require("path");
const client = require("@actions/artifact").default;

const root = process.env.GITHUB_WORKSPACE;
if (!root) {
  console.error("gha-upload-qr-artifact: GITHUB_WORKSPACE não definido.");
  process.exit(1);
}
const qrPath = path.join(root, "qr.html");
const qrWorkflowPath = path.join(root, "qr-workflow.html");
if (!fs.existsSync(qrPath)) {
  console.error("gha-upload-qr-artifact: qr.html não encontrado em", qrPath);
  process.exit(1);
}

const filesToUpload = [qrPath];
if (fs.existsSync(qrWorkflowPath)) {
  filesToUpload.push(qrWorkflowPath);
}

(async () => {
  try {
    // A API exige caminhos absolutos: ["qr.html"] resolve contra o cwd do Node (pasta do bot), não contra root.
    await client.uploadArtifact("whatsapp-qr", filesToUpload, root, {
      retentionDays: 3,
    });
    console.log(
      "Artifact 'whatsapp-qr' publicado (" +
        filesToUpload.map((f) => path.basename(f)).join(", ") +
        "). Veja na seção Artifacts desta execução."
    );
    process.exit(0);
  } catch (e) {
    console.error("gha-upload-qr-artifact:", e && e.message ? e.message : e);
    process.exit(1);
  }
})();
