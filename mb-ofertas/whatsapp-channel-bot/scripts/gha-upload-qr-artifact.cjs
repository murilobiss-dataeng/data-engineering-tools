/**
 * Upload antecipado no mesmo step (antes da espera de escaneamento), via @actions/artifact.
 * Requer ACTIONS_RUNTIME_TOKEN — use scripts/gha-export-actions-env.py no bash antes.
 */
const fs = require("fs");
const path = require("path");
const client = require("@actions/artifact").default;

const root = process.env.GITHUB_WORKSPACE;
if (!root) {
  console.error("gha-upload-qr-artifact: GITHUB_WORKSPACE não definido.");
  process.exit(1);
}
if (!process.env.ACTIONS_RUNTIME_TOKEN) {
  console.error("gha-upload-qr-artifact: ACTIONS_RUNTIME_TOKEN ausente.");
  process.exit(1);
}

const qrPath = path.join(root, "qr.html");
const qrWorkflowPath = path.join(root, "qr-workflow.html");
const qrWorkflowPngPath = path.join(root, "qr-workflow.png");
if (!fs.existsSync(qrPath)) {
  console.error("gha-upload-qr-artifact: qr.html não encontrado em", qrPath);
  process.exit(1);
}

const filesToUpload = [qrPath];
if (fs.existsSync(qrWorkflowPath)) filesToUpload.push(qrWorkflowPath);
if (fs.existsSync(qrWorkflowPngPath)) filesToUpload.push(qrWorkflowPngPath);

(async () => {
  try {
    await client.uploadArtifact("whatsapp-qr", filesToUpload, root, {
      retentionDays: 3,
    });
    console.log(
      "Artifact whatsapp-qr publicado:",
      filesToUpload.map((f) => path.basename(f)).join(", ")
    );
    process.exit(0);
  } catch (e) {
    console.error("gha-upload-qr-artifact:", e && e.message ? e.message : e);
    process.exit(1);
  }
})();
