/**
 * Usado só no GitHub Actions (Init WhatsApp): publica qr.html como artifact
 * imediatamente, sem esperar o fim do scan (o step principal continua em loop).
 *
 * Em alguns runners o Node não recebe ACTIONS_* no process.env; o toolkit lê só
 * process.env — hidratamos a partir de /proc (Linux) antes de carregar o client.
 */
const fs = require("fs");
const path = require("path");

function hydrateActionsEnvFromProc(pid) {
  if (process.platform !== "linux") return;
  const p = `/proc/${pid}/environ`;
  if (!fs.existsSync(p)) return;
  try {
    const buf = fs.readFileSync(p);
    const parts = buf.toString("binary").split("\0");
    for (const part of parts) {
      if (!part) continue;
      const eq = part.indexOf("=");
      if (eq <= 0) continue;
      const key = part.slice(0, eq);
      const val = part.slice(eq + 1);
      if (
        (key === "ACTIONS_RUNTIME_TOKEN" || key === "ACTIONS_RESULTS_URL") &&
        !process.env[key]
      ) {
        process.env[key] = val;
      }
    }
  } catch (_) {}
}

hydrateActionsEnvFromProc(process.pid);
hydrateActionsEnvFromProc(process.ppid);

const client = require("@actions/artifact").default;

const root = process.env.GITHUB_WORKSPACE;
if (!root) {
  console.error("gha-upload-qr-artifact: GITHUB_WORKSPACE não definido.");
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
if (fs.existsSync(qrWorkflowPath)) {
  filesToUpload.push(qrWorkflowPath);
}
if (fs.existsSync(qrWorkflowPngPath)) {
  filesToUpload.push(qrWorkflowPngPath);
}

(async () => {
  try {
    if (!process.env.ACTIONS_RUNTIME_TOKEN) {
      console.error(
        "gha-upload-qr-artifact: ACTIONS_RUNTIME_TOKEN ainda ausente (upload nativo do Actions indisponível neste processo)."
      );
      process.exit(1);
    }
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
