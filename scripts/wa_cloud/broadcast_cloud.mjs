import makeWASocket, { useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } from "@whiskeysockets/baileys";
import pino from "pino";
import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, "../..");
const AUTH_DIR = path.join(__dirname, "auth");
const CATALOG_PATH = path.join(ROOT_DIR, "deals", "data", "catalog.json");
const STATE_FILE = path.join(ROOT_DIR, "scripts", "whatsapp_posted.json");
const CHANNEL_INVITE = "0029Vb9DmoaEKyZLLKtLdc2I";

async function run() {
  if (process.env.WA_SESSION_BASE64) {
    console.log("Restoring WhatsApp session from environment secret...");
    fs.mkdirSync(AUTH_DIR, { recursive: true });
    const tarPath = path.join(__dirname, "session.tar.gz");
    fs.writeFileSync(tarPath, Buffer.from(process.env.WA_SESSION_BASE64, "base64"));
    execSync(`tar -xzf "${tarPath}" -C "${AUTH_DIR}"`);
  }

  if (!fs.existsSync(AUTH_DIR) || fs.readdirSync(AUTH_DIR).length === 0) {
    console.log("⚠️ No auth credentials found. Skipping WhatsApp broadcast.");
    process.exit(0);
  }

  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    logger: pino({ level: "silent" }),
    printQRInTerminal: false,
    auth: state,
    browser: ["TheBhom Cloud Bot", "Chrome", "1.0.0"]
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect } = update;

    if (connection === "open") {
      console.log("✅ WhatsApp Cloud Bot connected!");

      try {
        // Resolve Channel JID
        let channelJid = null;
        const jidFile = path.join(__dirname, "channel_jid.txt");
        if (fs.existsSync(jidFile)) {
          channelJid = fs.readFileSync(jidFile, "utf-8").trim();
        }

        if (!channelJid) {
          const meta = await sock.newsletterMetadata("invite", CHANNEL_INVITE);
          channelJid = meta.id;
          fs.writeFileSync(jidFile, channelJid);
          console.log(`Resolved Channel JID: ${channelJid}`);
        }

        // Get Top Deal
        let catalog = [];
        if (fs.existsSync(CATALOG_PATH)) {
          catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, "utf-8"));
        }

        let postedIds = new Set();
        if (fs.existsSync(STATE_FILE)) {
          try {
            postedIds = new Set(JSON.parse(fs.readFileSync(STATE_FILE, "utf-8")));
          } catch (e) {}
        }

        const candidate = catalog.find(item => {
          const id = item.asin || item.id;
          return id && !postedIds.has(id);
        });

        if (!candidate) {
          console.log("No new unposted deals found.");
          process.exit(0);
        }

        const id = candidate.asin || candidate.id;
        const title = candidate.title || "Loot Deal";
        const price = candidate.price || candidate.deal_price || 0;
        const originalPrice = candidate.original_price || candidate.mrp || 0;
        const discount = candidate.discount_percent || Math.round(((originalPrice - price) / (originalPrice || 1)) * 100);
        const store = candidate.store || "Amazon";
        const directUrl = candidate.affiliate_url || candidate.url || `https://www.amazon.in/dp/${id}?tag=bhom120704-21`;
        const slug = candidate.slug || id;
        const historyUrl = `https://thebhom.in/deals/p/${slug}.html`;

        const message = `🔥 *LOOT DEAL ALERT | THEBHOM* 🔥\n\n🛍️ *${title}*\n\n💰 *Deal Price: ₹${price}* ~₹${originalPrice}~ (🔥 *${discount}% OFF*)\n🏪 *Store:* ${store}\n\n⚡ *Direct Buy Link:*\n👉 ${directUrl}\n\n📊 *Check Price History:*\n👉 ${historyUrl}\n\n📢 *Official WhatsApp Channel:*\n👉 https://whatsapp.com/channel/${CHANNEL_INVITE}`;

        console.log(`Sending deal "${title}" to channel ${channelJid}...`);
        await sock.sendMessage(channelJid, { text: message });
        console.log("🎉 Deal successfully posted to WhatsApp Channel!");

        postedIds.add(id);
        fs.writeFileSync(STATE_FILE, JSON.stringify(Array.from(postedIds).slice(-500), null, 2));

      } catch (err) {
        console.error("Broadcast failed:", err);
      } finally {
        setTimeout(() => process.exit(0), 2000);
      }
    } else if (connection === "close") {
      const statusCode = (lastDisconnect?.error)?.output?.statusCode;
      if (statusCode === DisconnectReason.loggedOut) {
        console.log("Logged out of WhatsApp.");
      }
      process.exit(0);
    }
  });
}

run().catch(console.error);
