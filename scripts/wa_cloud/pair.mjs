import makeWASocket, { useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } from "@whiskeysockets/baileys";
import pino from "pino";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const AUTH_DIR = path.join(__dirname, "auth");

if (fs.existsSync(AUTH_DIR)) {
  fs.rmSync(AUTH_DIR, { recursive: true, force: true });
}
fs.mkdirSync(AUTH_DIR, { recursive: true });

async function startPairing() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    logger: pino({ level: "silent" }),
    printQRInTerminal: false,
    auth: state,
    browser: ["Ubuntu", "Chrome", "20.0.04"]
  });

  sock.ev.on("creds.update", saveCreds);

  let pairingCodeRequested = false;

  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (!sock.authState.creds.registered && !pairingCodeRequested) {
      pairingCodeRequested = true;
      setTimeout(async () => {
        try {
          const code = await sock.requestPairingCode("917987761789");
          console.log(`\n==============================================`);
          console.log(`🔑 WHATSAPP 24/7 PAIRING CODE: ${code}`);
          console.log(`==============================================\n`);
        } catch (err) {
          console.error("Pairing request error:", err);
        }
      }, 3000);
    }

    if (connection === "close") {
      const statusCode = (lastDisconnect?.error)?.output?.statusCode;
      console.log(`Connection closed (code: ${statusCode}). Reconnecting if valid...`);
      if (statusCode !== DisconnectReason.loggedOut) {
        startPairing();
      }
    } else if (connection === "open") {
      console.log("🎉 SUCCESS: WhatsApp 24/7 Headless Cloud Connected!");
      try {
        const metadata = await sock.newsletterMetadata("invite", "0029Vb9DmoaEKyZLLKtLdc2I");
        console.log(`✅ Found Channel: ${metadata.name} (JID: ${metadata.id})`);
        fs.writeFileSync(path.join(__dirname, "channel_jid.txt"), metadata.id);
      } catch (e) {
        console.log("Newsletter lookup status:", e.message);
      }
      process.exit(0);
    }
  });
}

startPairing().catch(console.error);
