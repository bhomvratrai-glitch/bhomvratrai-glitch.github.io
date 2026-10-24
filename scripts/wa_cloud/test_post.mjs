import makeWASocket, { useMultiFileAuthState, DisconnectReason, fetchLatestBaileysVersion } from "@whiskeysockets/baileys";
import pino from "pino";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, "../..");
const AUTH_DIR = path.join(__dirname, "auth");
const CATALOG_PATH = path.join(ROOT_DIR, "deals", "data", "catalog.json");
const CHANNEL_INVITE = "0029Vb9DmoaEKyZLLKtLdc2I";

async function testPost() {
  console.log("Connecting to WhatsApp session...");
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
      console.log("🎉 SUCCESS: WhatsApp is connected & authenticated!");

      try {
        console.log(`Resolving channel metadata for invite ${CHANNEL_INVITE}...`);
        const meta = await sock.newsletterMetadata("invite", CHANNEL_INVITE);
        const channelJid = meta.id;
        console.log(`✅ Channel Found: "${meta.name}" (JID: ${channelJid})`);
        fs.writeFileSync(path.join(__dirname, "channel_jid.txt"), channelJid);

        // Fetch top deal
        let catalog = [];
        if (fs.existsSync(CATALOG_PATH)) {
          catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, "utf-8"));
        }

        const topDeal = catalog[0] || {
          title: "Workout BBL Jackets for Women Cropped Gym Athletic Tops",
          asin: "B0BZLNQXN2",
          price: 4525,
          original_price: 905194,
          discount_percent: 100,
          store: "Amazon",
          slug: "workout-bbl-jackets-for-women-cropped-gym-athletic-amz-b0bzlnqxn2"
        };

        const title = topDeal.title;
        const price = topDeal.price || topDeal.deal_price;
        const mrp = topDeal.original_price || topDeal.mrp || (price * 2);
        const discount = topDeal.discount_percent || 70;
        const directUrl = `https://www.amazon.in/dp/${topDeal.asin}?tag=bhom120704-21`;
        const historyUrl = `https://thebhom.in/deals/p/${topDeal.slug}.html`;

        const welcomePost = `🔥 *WELCOME TO THEBHOM DEALS OFFICIAL CHANNEL!* 🔥\n\nVerified 70% to 100% OFF loot drops, price crashes & flash sales are now active 24/7!\n\n🛍️ *${title}*\n\n💰 *Deal Price: ₹${price}* ~₹${mrp}~ (🔥 *${discount}% OFF*)\n🏪 *Store:* Amazon India\n\n⚡ *Direct Buy Link:*\n👉 ${directUrl}\n\n📊 *Check Price History:*\n👉 ${historyUrl}\n\n📢 *Invite Link:*\n👉 https://whatsapp.com/channel/${CHANNEL_INVITE}`;

        console.log("🚀 Sending live post to WhatsApp Channel...");
        const result = await sock.sendMessage(channelJid, { text: welcomePost });
        console.log("✅ LIVE POST SENT SUCCESSFULLY TO WHATSAPP CHANNEL!", result?.key?.id || "");

      } catch (err) {
        console.error("Error during channel broadcast:", err);
      } finally {
        setTimeout(() => {
          sock.end();
          process.exit(0);
        }, 3000);
      }
    } else if (connection === "close") {
      const statusCode = (lastDisconnect?.error)?.output?.statusCode;
      console.log(`Connection closed (code: ${statusCode}).`);
      if (statusCode === DisconnectReason.loggedOut) {
        console.log("Logged out.");
        process.exit(1);
      }
    }
  });
}

testPost().catch(console.error);
