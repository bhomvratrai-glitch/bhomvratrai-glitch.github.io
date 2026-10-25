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
const DEFAULT_WA_LINK = `https://whatsapp.com/channel/${CHANNEL_INVITE}`;

function restoreSessionIfCloud() {
  if (process.env.WA_SESSION_BASE64 && (!fs.existsSync(AUTH_DIR) || fs.readdirSync(AUTH_DIR).length === 0)) {
    console.log("[WhatsApp] Restoring WhatsApp session from WA_SESSION_BASE64 secret...");
    fs.mkdirSync(AUTH_DIR, { recursive: true });
    const tarPath = path.join(__dirname, "session.tar.gz");
    fs.writeFileSync(tarPath, Buffer.from(process.env.WA_SESSION_BASE64, "base64"));
    execSync(`tar -xzf "${tarPath}" -C "${AUTH_DIR}"`);
  }
}

function parseCliArgs() {
  const args = process.argv.slice(2);
  let item = null;

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--json" && args[i + 1]) {
      try {
        item = JSON.parse(args[i + 1]);
      } catch (e) {
        console.error("[WhatsApp] Failed to parse --json argument:", e);
      }
      i++;
    } else if (args[i] === "--file" && args[i + 1]) {
      try {
        const fileContent = fs.readFileSync(args[i + 1], "utf-8");
        item = JSON.parse(fileContent);
      } catch (e) {
        console.error("[WhatsApp] Failed to read --file:", e);
      }
      i++;
    }
  }
  return item;
}

function formatWhatsAppMessage(item) {
  const type = item.type || "deal";

  if (type === "news") {
    const title = item.title || "Breaking News";
    const desc = item.desc || "";
    const url = item.url || "https://thebhom.in/news/";

    return (
      `🚨 *BREAKING NEWS | THEBHOM*\n\n` +
      `*${title}*\n\n` +
      `${desc}\n\n` +
      `👉 *पूरी खबर यहाँ पढ़ें:*\n${url}\n\n` +
      `🌐 *TheBhom.in पर ताज़ा अपडेट्स:*\nhttps://thebhom.in/news/\n\n` +
      `📢 *Official WhatsApp Channel:*\n${DEFAULT_WA_LINK}`
    );
  }

  // Deal Format
  const title = item.title || "Loot Deal Alert";
  const price = item.price ? `₹${item.price}` : "Loot Price";
  const mrp = item.mrp && item.mrp !== item.price ? ` ~₹${item.mrp}~` : "";
  const discount = item.discount ? ` (🔥 *${item.discount}% OFF*)` : "";
  const store = item.store || "Amazon India";
  const storeUrl = item.store_url || item.profitLink || item.url || "https://thebhom.in/deals/";
  const pageUrl = item.page_url || item.dedicatedPage || "https://thebhom.in/deals/";

  return (
    `🔥 *LOOT DEAL ALERT | THEBHOM* 🔥\n\n` +
    `🛍️ *${title}*\n\n` +
    `💰 *Deal Price: ${price}*${mrp}${discount}\n` +
    `🏪 *Store:* ${store}\n\n` +
    `⚡ *1-Click Direct Store Purchase:*\n` +
    `👉 ${storeUrl}\n\n` +
    `🌐 *Check Price History & Live Tracker:*\n` +
    `👉 ${pageUrl}\n\n` +
    `📢 *Join WhatsApp Channel for 24/7 Loot Drops:*\n` +
    `👉 ${DEFAULT_WA_LINK}`
  );
}

async function getImageBuffer(imageUrl) {
  if (!imageUrl || typeof imageUrl !== "string") return null;
  try {
    let cleanUrl = imageUrl.trim();
    if (cleanUrl.startsWith("//")) cleanUrl = "https:" + cleanUrl;
    if (!cleanUrl.startsWith("http")) return null;

    const res = await fetch(cleanUrl, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
      },
      signal: AbortSignal.timeout(8000)
    });
    if (!res.ok) return null;
    const arrayBuffer = await res.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    return buffer.length > 500 ? buffer : null;
  } catch (err) {
    console.error("[WhatsApp] Could not fetch image buffer:", err.message);
    return null;
  }
}

async function run() {
  restoreSessionIfCloud();

  if (!fs.existsSync(AUTH_DIR) || fs.readdirSync(AUTH_DIR).length === 0) {
    console.log("⚠️ No WhatsApp auth credentials found. Skipping WhatsApp broadcast.");
    process.exit(0);
  }

  let item = parseCliArgs();

  // If no direct item provided via CLI, load top unposted deal from catalog
  if (!item) {
    let catalog = [];
    if (fs.existsSync(CATALOG_PATH)) {
      try {
        catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, "utf-8"));
      } catch (e) {}
    }

    let postedIds = new Set();
    if (fs.existsSync(STATE_FILE)) {
      try {
        postedIds = new Set(JSON.parse(fs.readFileSync(STATE_FILE, "utf-8")));
      } catch (e) {}
    }

    const candidate = catalog.find((c) => {
      const id = c.asin || c.id;
      return id && !postedIds.has(id);
    });

    if (!candidate) {
      console.log("[WhatsApp] No new unposted deals found in catalog.");
      process.exit(0);
    }

    const id = candidate.asin || candidate.id;
    const title = candidate.title || "Loot Deal";
    const price = candidate.price || candidate.deal_price || 0;
    const mrp = candidate.original_price || candidate.mrp || 0;
    const discount = candidate.discount_percent || candidate.discountNum || Math.round(((mrp - price) / (mrp || 1)) * 100);
    const store = candidate.store || "Amazon";
    let directUrl = candidate.profitLink || candidate.affiliate_url || candidate.url || `https://www.amazon.in/dp/${id}?tag=bhom120704-21`;
    if (directUrl.includes("amazon.in") && !directUrl.includes("tag=")) {
      directUrl += directUrl.includes("?") ? "&tag=bhom120704-21" : "?tag=bhom120704-21";
    }
    const slug = candidate.slug || id;
    const pageUrl = candidate.dedicatedPage || `https://thebhom.in/deals/p/${slug}.html`;
    const img = candidate.cleanImage || candidate.image || "";

    item = {
      id: id,
      type: "deal",
      title: title,
      price: price,
      mrp: mrp,
      discount: discount,
      store: store,
      store_url: directUrl,
      page_url: pageUrl,
      image: img
    };
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
      try {
        let channelJid = null;
        const jidFile = path.join(__dirname, "channel_jid.txt");
        if (fs.existsSync(jidFile)) {
          channelJid = fs.readFileSync(jidFile, "utf-8").trim();
        }

        if (!channelJid) {
          const meta = await sock.newsletterMetadata("invite", CHANNEL_INVITE);
          channelJid = meta.id;
          fs.writeFileSync(jidFile, channelJid);
        }

        const message = formatWhatsAppMessage(item);
        const imageUrl = item.image || item.cleanImage;
        let imageBuffer = null;

        if (imageUrl) {
          console.log(`[WhatsApp] Fetching product image buffer: ${imageUrl.slice(0, 60)}...`);
          imageBuffer = await getImageBuffer(imageUrl);
        }

        if (imageBuffer) {
          console.log(`[WhatsApp] Sending product image + caption to channel ${channelJid}...`);
          await sock.sendMessage(channelJid, {
            image: imageBuffer,
            caption: message
          });
          console.log(`✅ [WhatsApp Channel Sent with Image]: ${item.title?.slice(0, 45)}`);
        } else {
          console.log(`[WhatsApp] Sending deal text to channel ${channelJid}...`);
          await sock.sendMessage(channelJid, { text: message });
          console.log(`✅ [WhatsApp Channel Sent]: ${item.title?.slice(0, 45)}`);
        }

        // Record in state file
        if (item.id) {
          let postedIds = new Set();
          if (fs.existsSync(STATE_FILE)) {
            try {
              postedIds = new Set(JSON.parse(fs.readFileSync(STATE_FILE, "utf-8")));
            } catch (e) {}
          }
          postedIds.add(String(item.id).replace("deal_", ""));
          fs.writeFileSync(STATE_FILE, JSON.stringify(Array.from(postedIds).slice(-500), null, 2));
        }

        setTimeout(() => {
          sock.end();
          process.exit(0);
        }, 1500);

      } catch (err) {
        console.error("[WhatsApp] Broadcast failed:", err);
        setTimeout(() => {
          sock.end();
          process.exit(1);
        }, 1000);
      }
    } else if (connection === "close") {
      const statusCode = (lastDisconnect?.error)?.output?.statusCode;
      if (statusCode === DisconnectReason.loggedOut) {
        console.log("[WhatsApp] Logged out.");
        process.exit(1);
      }
      process.exit(0);
    }
  });
}

run().catch((err) => {
  console.error("[WhatsApp Fatal]", err);
  process.exit(1);
});
