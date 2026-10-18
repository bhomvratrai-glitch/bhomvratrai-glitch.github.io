// Cloudflare Pages Function: /api/admin
// Secure Owner / Admin Backend restricted exclusively to bhomvratrai7225@gmail.com

const NEON_SQL_URL = 'https://ep-gentle-lab-awk96f6x-pooler.c-12.us-east-1.aws.neon.tech/sql';
const DEFAULT_CONN_STR = 'postgresql://neondb_owner:npg_yAGWlbrK5PN6@ep-gentle-lab-awk96f6x-pooler.c-12.us-east-1.aws.neon.tech/neondb?sslmode=require';
const OWNER_EMAIL = 'bhomvratrai7225@gmail.com';
const DEFAULT_PASSKEY = 'Bhomvrat@123'; // Master Owner Passkey

function esc(val) {
  if (val === null || val === undefined) return 'NULL';
  if (typeof val === 'number') return Number.isFinite(val) ? String(val) : '0';
  return "'" + String(val).replace(/'/g, "''").replace(/\\/g, '\\\\') + "'";
}

async function queryNeon(env, sql) {
  const connStr = env?.DATABASE_URL || DEFAULT_CONN_STR;
  const res = await fetch(NEON_SQL_URL, {
    method: 'POST',
    headers: {
      'neon-connection-string': connStr,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: sql }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Neon SQL Error: ${text}`);
  }
  return res.json();
}

function verifyOwnerAuth(request, env) {
  const masterKey = env?.ADMIN_PASSKEY || DEFAULT_PASSKEY;
  const authHeader = request.headers.get('Authorization') || '';
  const emailHeader = (request.headers.get('x-owner-email') || '').trim().toLowerCase();

  // Allow Bearer token match
  const token = authHeader.replace(/^Bearer\s+/i, '').trim();
  if (emailHeader === OWNER_EMAIL && token === `tb_owner_${masterKey}`) {
    return true;
  }
  return false;
}

export async function onRequestPost(context) {
  try {
    const { request, env } = context;
    const body = await request.json().catch(() => ({}));
    const { action } = body;
    const masterKey = env?.ADMIN_PASSKEY || DEFAULT_PASSKEY;

    // 1. Owner Login
    if (action === 'login') {
      const email = (body.email || '').trim().toLowerCase();
      const passkey = (body.passkey || '').trim();

      if (email !== OWNER_EMAIL) {
        return new Response(
          JSON.stringify({ error: 'Access Denied: Only bhomvratrai7225@gmail.com is authorized.' }),
          { status: 403, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
        );
      }

      if (passkey !== masterKey) {
        return new Response(
          JSON.stringify({ error: 'Invalid Owner Passkey' }),
          { status: 401, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
        );
      }

      const sessionToken = `tb_owner_${masterKey}`;
      return new Response(
        JSON.stringify({
          success: true,
          token: sessionToken,
          owner: OWNER_EMAIL,
          message: 'Welcome Bhom Vrat Rai! Owner dashboard unlocked.',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // Security Gate: verify owner session for all subsequent actions
    if (!verifyOwnerAuth(request, env)) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized: Owner credentials required.' }),
        { status: 403, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // 2. Fetch Dashboard Data & Stats
    if (action === 'get_dashboard') {
      const ordersRes = await queryNeon(
        env,
        `SELECT id, user_name, user_email, user_phone, product_id, product_name, amount, utr_number, status, license_key, admin_notes, created_at, updated_at
         FROM payment_orders
         ORDER BY created_at DESC
         LIMIT 200;`
      );

      const statsRes = await queryNeon(
        env,
        `SELECT
           COUNT(*) AS total_orders,
           COUNT(*) FILTER (WHERE status = 'PENDING') AS pending_orders,
           COUNT(*) FILTER (WHERE status = 'APPROVED') AS approved_orders,
           COALESCE(SUM(amount) FILTER (WHERE status = 'APPROVED'), 0) AS total_revenue,
           COALESCE(SUM(amount) FILTER (WHERE status = 'APPROVED' AND created_at >= CURRENT_DATE), 0) AS today_revenue
         FROM payment_orders;`
      );

      const stats = statsRes.rows?.[0] || {
        total_orders: 0,
        pending_orders: 0,
        approved_orders: 0,
        total_revenue: 0,
        today_revenue: 0,
      };

      return new Response(
        JSON.stringify({
          success: true,
          stats: {
            totalOrders: parseInt(stats.total_orders, 10) || 0,
            pendingOrders: parseInt(stats.pending_orders, 10) || 0,
            approvedOrders: parseInt(stats.approved_orders, 10) || 0,
            totalRevenue: parseFloat(stats.total_revenue) || 0,
            todayRevenue: parseFloat(stats.today_revenue) || 0,
          },
          orders: ordersRes.rows || [],
        }),
        { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // 2.5 Fetch Real-Time Telemetry Analytics (Pinterest Style, 100% Real Live Data)
    if (action === 'get_analytics') {
      const timeframe = (body.timeframe || '30d').toLowerCase();
      let timeSql = "created_at >= NOW() - INTERVAL '30 days'";
      if (timeframe === '24h') timeSql = "created_at >= NOW() - INTERVAL '24 hours'";
      else if (timeframe === '7d') timeSql = "created_at >= NOW() - INTERVAL '7 days'";
      else if (timeframe === '90d') timeSql = "created_at >= NOW() - INTERVAL '90 days'";
      else if (timeframe === 'all') timeSql = '1=1';

      // 1. Overview metrics
      const overviewRes = await queryNeon(
        env,
        `SELECT
           COUNT(*) FILTER (WHERE event_type = 'impression') AS impressions,
           COUNT(*) FILTER (WHERE event_type = 'engagement') AS engagements,
           COUNT(*) FILTER (WHERE event_type = 'outbound_click') AS outbound_clicks,
           COUNT(*) FILTER (WHERE event_type = 'save') AS saves,
           COUNT(DISTINCT visitor_id) AS total_audience,
           COUNT(DISTINCT visitor_id) FILTER (WHERE event_type IN ('engagement', 'outbound_click', 'save')) AS engaged_audience,
           COUNT(DISTINCT visitor_id) FILTER (WHERE created_at >= NOW() - INTERVAL '15 minutes') AS realtime_active
         FROM site_events
         WHERE ${timeSql};`
      );

      // 2. Section breakdown
      const sectionRes = await queryNeon(
        env,
        `SELECT
           section,
           COUNT(*) FILTER (WHERE event_type = 'impression') AS impressions,
           COUNT(*) FILTER (WHERE event_type = 'engagement') AS engagements,
           COUNT(*) FILTER (WHERE event_type = 'outbound_click') AS outbound_clicks,
           COUNT(*) FILTER (WHERE event_type = 'save') AS saves,
           COUNT(DISTINCT visitor_id) AS total_audience
         FROM site_events
         WHERE ${timeSql}
         GROUP BY section
         ORDER BY impressions DESC;`
      );

      // 3. Top outbound click destinations
      const topOutboundRes = await queryNeon(
        env,
        `SELECT target_url, COUNT(*) AS clicks
         FROM site_events
         WHERE event_type = 'outbound_click' AND target_url IS NOT NULL AND ${timeSql}
         GROUP BY target_url
         ORDER BY clicks DESC
         LIMIT 10;`
      );

      // 4. Recent live events stream
      const recentEventsRes = await queryNeon(
        env,
        `SELECT id, event_type, section, page_path, target_url, visitor_id, created_at
         FROM site_events
         ORDER BY created_at DESC
         LIMIT 15;`
      );

      const r = overviewRes.rows?.[0] || {};
      const impressions = parseInt(r.impressions, 10) || 0;
      const engagements = parseInt(r.engagements, 10) || 0;
      const outboundClicks = parseInt(r.outbound_clicks, 10) || 0;
      const saves = parseInt(r.saves, 10) || 0;
      const totalAudience = parseInt(r.total_audience, 10) || 0;
      const engagedAudience = parseInt(r.engaged_audience, 10) || 0;
      const realtimeActive = parseInt(r.realtime_active, 10) || 0;

      const engagementRate = impressions > 0 ? ((engagements / impressions) * 100).toFixed(2) : '0.00';
      const outboundCtr = impressions > 0 ? ((outboundClicks / impressions) * 100).toFixed(2) : '0.00';

      return new Response(
        JSON.stringify({
          success: true,
          timeframe,
          overview: {
            impressions,
            engagements,
            outboundClicks,
            saves,
            totalAudience,
            engagedAudience,
            realtimeActive,
            engagementRate,
            outboundCtr,
          },
          sections: sectionRes.rows || [],
          topOutbound: topOutboundRes.rows || [],
          recentEvents: recentEventsRes.rows || [],
        }),
        { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // 3. Approve Order
    if (action === 'approve') {
      const { orderId } = body;
      if (!orderId) {
        return new Response(JSON.stringify({ error: 'Order ID is required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        });
      }

      const licenseKey = `TB-PRO-${orderId.replace(/[^A-Za-z0-9]/g, '').slice(-8)}-${Math.random().toString(36).substring(2, 6).toUpperCase()}`;

      await queryNeon(
        env,
        `UPDATE payment_orders
         SET status = 'APPROVED', license_key = ${esc(licenseKey)}, updated_at = NOW()
         WHERE id = ${esc(orderId.trim())};`
      );

      return new Response(
        JSON.stringify({
          success: true,
          orderId,
          licenseKey,
          message: `Order ${orderId} approved and access key generated.`,
        }),
        { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // 4. Reject Order
    if (action === 'reject') {
      const { orderId, reason = 'Invalid UTR or payment not received in bank.' } = body;
      if (!orderId) {
        return new Response(JSON.stringify({ error: 'Order ID is required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        });
      }

      await queryNeon(
        env,
        `UPDATE payment_orders
         SET status = 'REJECTED', admin_notes = ${esc(reason)}, updated_at = NOW()
         WHERE id = ${esc(orderId.trim())};`
      );

      return new Response(
        JSON.stringify({ success: true, orderId, message: `Order ${orderId} marked as rejected.` }),
        { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // 5. Manual Grant
    if (action === 'manual_grant') {
      const { userEmail, userName = 'VIP Customer', productName = 'ToolNest VIP Lifetime', amount = 0 } = body;
      if (!userEmail) {
        return new Response(JSON.stringify({ error: 'User email is required' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        });
      }

      const randomSuffix = Math.random().toString(36).substring(2, 6).toUpperCase();
      const orderId = `TB-MANUAL-${Date.now().toString(36).toUpperCase()}-${randomSuffix}`;
      const licenseKey = `TB-VIP-GIFT-${randomSuffix}`;

      await queryNeon(
        env,
        `INSERT INTO payment_orders (id, user_name, user_email, product_id, product_name, amount, utr_number, status, license_key, admin_notes)
         VALUES (
           ${esc(orderId)},
           ${esc(userName)},
           ${esc(userEmail.trim().toLowerCase())},
           'manual-gift',
           ${esc(productName)},
           ${parseFloat(amount) || 0},
           'OWNER_DIRECT_GRANT',
           'APPROVED',
           ${esc(licenseKey)},
           'Granted directly by Owner'
         );`
      );

      return new Response(
        JSON.stringify({
          success: true,
          orderId,
          licenseKey,
          message: `Access granted successfully to ${userEmail}!`,
        }),
        { status: 201, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    return new Response(JSON.stringify({ error: 'Invalid action' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error', details: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-owner-email',
    },
  });
}
