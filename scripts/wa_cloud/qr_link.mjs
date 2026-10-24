import makeWASocket, { useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } from "@whiskeysockets/baileys";
import pino from "pino";
import fs from "fs";
import path from "path";
import QRCode from "qrcode";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = path.join(__dirname, "auth");
const QR_PATH = "/tmp/whatsapp_cloud_qr.png";

if (fs.existsSync(AUTH_DIR)) {
  fs.rmSync(AUTH_DIR, { recursive: true, force: true });
}
fs.mkdirSync(AUTH_DIR, { recursive: true });

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    logger: pino({ level: "silent" }),
    printQRInTerminal: true,
    auth: state,
    browser: ["TheBhom Cloud Bot", "Chrome", "1.0.0"]
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log("\n📱 Generating WhatsApp QR Code for 24/7 Cloud Session...");
      await QRCode.toFile(QR_PATH, qr, { width: 450 });
      try {
        execSync(`open ${QR_PATH}`);
      } catch (e) {}
      console.log(`\n======================================================`);
      console.log(`👉 QR Code opened on your Mac screen!`);
      console.log(`Open WhatsApp on phone -> Linked Devices -> Scan this QR`);
      console.log(`======================================================\n`);
    }

    if (connection === "close") {
      const statusCode = (lastDisconnect?.error)?.output?.statusCode;
      if (statusCode !== DisconnectReason.loggedOut) {
        start();
      }
    } else if (connection === "open") {
      console.log("\n🎉 SUCCESS: WhatsApp 24/7 Cloud Session Connected!");
      try {
        execSync("pkill -f 'Preview.*whatsapp_cloud_qr'");
      } catch (e) {}

      try {
        const metadata = await sock.newsletterMetadata("invite", "0029Vb9DmoaEKyZLLKtLdc2I");
        console.log(`✅ Channel Resolved: ${metadata.name} (ID: ${metadata.id})`);
        fs.writeFileSync(path.join(__dirname, "channel_jid.txt"), metadata.id);
      } catch (err) {
        console.log("Channel metadata lookup:", err.message);
      }

      console.log("Packaging auth session into tar.gz...");
      const tarPath = path.join(__dirname, "auth.tar.gz");
      execSync(`tar -czf "${tarPath}" -C "${AUTH_DIR}" .`);
      const base64Session = fs.readFileSync(tarPath).toString("base64");
      
      console.log("Uploading session to GitHub Secrets (WA_SESSION_BASE64)...");
      try {
        execSync(`echo "${base64Session}" | gh secret set WA_SESSION_BASE64 -R bhomvratrai-glitch/thebhom-landing`);
        console.log("✅ Secret WA_SESSION_BASE64 uploaded to GitHub successfully!");
      } catch (err) {
        console.error("gh secret upload error:", err.message);
      }

      console.log("Cloud setup 100% complete!");
      process.exit(0);
    }
  });
}

start().catch(console.error);
