export async function onRequest(context) {
  const { request, next, env } = context;

  // Cloudflare automatically populates this header with the visitor's real IP
  const ip = request.headers.get('CF-Connecting-IP') || 'Unknown';
  const url = new URL(request.url);
  const timestamp = new Date().toISOString();

  // Optional: Skip logging static assets (CSS, JS, images) so you only log page visits
  const isAsset = /\.(css|js|png|jpg|jpeg|gif|svg|ico|woff2?)$/i.test(url.pathname);

  if (!isAsset) {
    // 1. Log to Cloudflare Dashboard (Real-time & Workers Logs)
    console.log(JSON.stringify({ timestamp, ip, path: url.pathname }));

    // 2. Optional: Save permanently to Cloudflare KV (requires a KV binding named IP_LOGS)
    // const key = `${timestamp}_${crypto.randomUUID()}`;
    // context.waitUntil(env.IP_LOGS.put(key, JSON.stringify({ timestamp, ip, path: url.pathname })));
  }

  // Continue serving the normal static page
  return next();
}

