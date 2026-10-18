// Cloudflare Pages Function: /api/orders
// Handles customer order creation and real-time status checks

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

export async function onRequestPost(context) {
  try {
    const { request, env } = context;
    const body = await request.json().catch(() => ({}));
    const rawUtr = body.utrNumber || body.utr || body.txnId || '';
    const rawEmail = body.userEmail || body.email || '';
    const rawName = body.userName || body.name || (rawEmail ? rawEmail.split('@')[0] : 'Customer');
    const rawProduct = body.productName || body.title || body.plan || 'TheBhom Pro';
    const rawProductId = body.productId || (rawProduct.toLowerCase().includes('business') ? 'business' : 'pro');
    const rawAmount = body.amount || 199;
    const userPhone = body.userPhone || body.phone || '';

    const trimmedUtr = String(rawUtr).trim();
    const trimmedEmail = String(rawEmail).trim().toLowerCase();
    const trimmedName = String(rawName).trim();
    const productName = String(rawProduct).trim();
    const productId = String(rawProductId).trim();

    if (!trimmedUtr) {
      return new Response(JSON.stringify({ error: 'UTR / Transaction ID is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    if (!trimmedEmail) {
      return new Response(JSON.stringify({ error: 'Email is required for order delivery' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    // Check if duplicate UTR already exists
    const checkSql = `SELECT id, status, license_key, product_name FROM payment_orders WHERE utr_number = ${esc(trimmedUtr)} LIMIT 1;`;
    const existing = await queryNeon(env, checkSql);

    if (existing.rows && existing.rows.length > 0) {
      const row = existing.rows[0];
      return new Response(
        JSON.stringify({
          success: true,
          isExisting: true,
          orderId: row.id,
          status: row.status,
          licenseKey: row.license_key,
          productName: row.product_name,
        }),
        { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // Generate unique Order ID
    const randomSuffix = Math.random().toString(36).substring(2, 6).toUpperCase();
    const orderId = `TB-${Date.now().toString(36).toUpperCase()}-${randomSuffix}`;
    const parsedAmount = Math.max(0, parseFloat(rawAmount) || 49);

    const insertSql = `
      INSERT INTO payment_orders (id, user_name, user_email, user_phone, product_id, product_name, amount, utr_number, status)
      VALUES (
        ${esc(orderId)},
        ${esc(trimmedName || 'Valued Customer')},
        ${esc(trimmedEmail)},
        ${esc(userPhone ? userPhone.trim() : '')},
        ${esc(productId)},
        ${esc(productName)},
        ${parsedAmount},
        ${esc(trimmedUtr)},
        'PENDING'
      );
    `;

    await queryNeon(env, insertSql);

    return new Response(
      JSON.stringify({
        success: true,
        orderId,
        status: 'PENDING',
        message: 'Order submitted and pending owner verification',
      }),
      { status: 201, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
    );
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Server error', details: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    });
  }
}

export async function onRequestGet(context) {
  try {
    const { request, env } = context;
    const url = new URL(request.url);
    const orderId = url.searchParams.get('id') || url.searchParams.get('orderId');
    const utr = url.searchParams.get('utr');
    const email = url.searchParams.get('email');

    if (!orderId && !utr && !email) {
      return new Response(JSON.stringify({ error: 'Order ID, UTR or email required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    let query = `SELECT id, user_name, user_email, product_id, product_name, amount, utr_number, status, license_key, created_at, updated_at FROM payment_orders WHERE `;
    if (orderId) {
      query += `id = ${esc(orderId.trim())} LIMIT 1;`;
    } else if (utr) {
      query += `utr_number = ${esc(utr.trim())} LIMIT 1;`;
    } else {
      query += `LOWER(user_email) = ${esc(email.trim().toLowerCase())} ORDER BY created_at DESC LIMIT 1;`;
    }

    const data = await queryNeon(env, query);
    if (!data.rows || data.rows.length === 0) {
      return new Response(JSON.stringify({ found: false, message: 'Order not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    const order = data.rows[0];
    return new Response(
      JSON.stringify({
        found: true,
        order: {
          id: order.id,
          userName: order.user_name,
          userEmail: order.user_email,
          productId: order.product_id,
          productName: order.product_name,
          amount: parseFloat(order.amount),
          utrNumber: order.utr_number,
          status: order.status,
          licenseKey: order.license_key,
          createdAt: order.created_at,
          isApproved: order.status === 'APPROVED',
        },
      }),
      { status: 200, headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } }
    );
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
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
