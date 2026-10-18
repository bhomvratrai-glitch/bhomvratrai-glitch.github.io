// Cloudflare Pages Function: /api/track
// High-performance real-time analytics telemetry ingestion for TheBhom

const NEON_SQL_URL = 'https://ep-gentle-lab-awk96f6x-pooler.c-12.us-east-1.aws.neon.tech/sql';
const DEFAULT_CONN_STR = 'postgresql://neondb_owner:npg_yAGWlbrK5PN6@ep-gentle-lab-awk96f6x-pooler.c-12.us-east-1.aws.neon.tech/neondb?sslmode=require';

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

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestPost(context) {
  try {
    const { request, env } = context;
    let body = {};
    const contentType = request.headers.get('content-type') || '';
    
    if (contentType.includes('application/json')) {
      body = await request.json().catch(() => ({}));
    } else {
      const text = await request.text().catch(() => '');
      try {
        body = JSON.parse(text);
      } catch {
        body = {};
      }
    }

    const eventType = String(body.event_type || body.event || 'impression').trim().toLowerCase();
    const validEvents = ['impression', 'engagement', 'outbound_click', 'save'];
    const safeEvent = validEvents.includes(eventType) ? eventType : 'engagement';

    const section = String(body.section || 'home').trim().toLowerCase().slice(0, 50);
    const pagePath = String(body.page_path || body.path || '/').trim().slice(0, 500);
    const targetUrl = body.target_url ? String(body.target_url).trim().slice(0, 1000) : null;
    const visitorId = String(body.visitor_id || 'anon_' + Math.random().toString(36).substring(2, 12)).trim().slice(0, 64);
    const sessionId = body.session_id ? String(body.session_id).trim().slice(0, 64) : null;
    const referrer = body.referrer ? String(body.referrer).trim().slice(0, 500) : null;
    
    const metaObj = (body.meta && typeof body.meta === 'object') ? body.meta : {};
    // Auto-attach CF country / city if present
    const cf = request.cf || {};
    if (cf.country) metaObj.country = cf.country;
    if (cf.city) metaObj.city = cf.city;
    if (cf.deviceType) metaObj.device = cf.deviceType;
    const metaJson = JSON.stringify(metaObj);

    const sql = `INSERT INTO site_events (event_type, section, page_path, target_url, visitor_id, session_id, referrer, meta)
      VALUES (${esc(safeEvent)}, ${esc(section)}, ${esc(pagePath)}, ${esc(targetUrl)}, ${esc(visitorId)}, ${esc(sessionId)}, ${esc(referrer)}, ${esc(metaJson)}::jsonb);`;

    // Asynchronously insert into Neon
    await queryNeon(env, sql);

    return new Response(JSON.stringify({ success: true, recorded: safeEvent }), {
      status: 200,
      headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
    });
  } catch (err) {
    // Non-blocking telemetry response
    return new Response(JSON.stringify({ success: false, error: err.message }), {
      status: 200, // Return 200 to prevent client errors
      headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS,
  });
}
