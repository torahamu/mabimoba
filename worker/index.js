// Mobilay v2.1.5 catalog-only HTTPS mirror (Cloudflare Workers)
// Japanese translation data hosted on GitHub Pages:
// https://torahamu.github.io/mabimoba/api/json/
// All other /api/json/*.enc are fetched from the original API.
// This Worker never forwards authorization or cookies.
const ORIGIN = 'https://api.mobilay.kr/api/json/';
const PAGES = 'https://torahamu.github.io/mabimoba/api/json/';
const OVERRIDES = new Set([
  'dps_skill_names_tw.enc',
  'dps_buff_names_tw.enc',
  'barter_exchange_catalog_tw.enc',
  'item_lookup_catalog_tw.enc',
]);

export default {
  async fetch(request) {
    const sourceUrl = new URL(request.url);
    const route = /^\/api\/json\/([A-Za-z0-9_]+\.enc)$/.exec(sourceUrl.pathname);
    if (request.method !== 'GET' || !route) {
      return new Response('Not found', { status: 404 });
    }
    const name = route[1];
    const fromPages = OVERRIDES.has(name);
    const target = new URL(name, fromPages ? PAGES : ORIGIN);
    if (sourceUrl.searchParams.has('t')) {
      target.searchParams.set('t', sourceUrl.searchParams.get('t'));
    }
    const headers = new Headers();
    if (!fromPages) {
      for (const key of ['X-Lay-App', 'X-Lay-Key', 'User-Agent']) {
        const val = request.headers.get(key);
        if (val) headers.set(key, val);
      }
    }
    let upstream;
    try {
      upstream = await fetch(target.toString(), { method: 'GET', headers, redirect: 'follow' });
    } catch (_) {
      return new Response('Upstream request failed', { status: 502 });
    }
    if (!upstream.ok) {
      return new Response(`Upstream HTTP ${upstream.status}`, { status: 502 });
    }
    return new Response(upstream.body, {
      status: 200,
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-store',
        'X-Mobilay-Mirror-Source': fromPages ? 'github-pages' : 'upstream',
      },
    });
  },
};
