// Form tiket (/api/tickets) di Cloudflare Pages: diteruskan ke service tiket di Raspberry Pi lewat tunnel.
// Database tiket tetap di Pi. TICKET_ORIGIN bisa diatur di pengaturan proyek Pages.
export async function onRequest({ request, env }) {
  const origin = (env.TICKET_ORIGIN || 'https://tiket.altora.id').replace(/\/$/, '');
  const headers = new Headers();
  for (const h of ['content-type', 'accept']) {
    const v = request.headers.get(h);
    if (v) headers.set(h, v);
  }
  // service tiket hanya mengizinkan origin altora.id untuk CORS; permintaan ini server-ke-server
  headers.set('origin', 'https://altora.id');
  const ip = request.headers.get('cf-connecting-ip');
  if (ip) headers.set('x-forwarded-for', ip);
  const init = { method: request.method, headers };
  if (!['GET', 'HEAD'].includes(request.method)) init.body = await request.arrayBuffer();
  const down = () => Response.json({ ok: false, error: 'Layanan tiket sedang tidak bisa dihubungi. Silakan hubungi kami lewat WhatsApp.' },
    { status: 502, headers: { 'cache-control': 'no-store' } });
  let res;
  try {
    res = await fetch(origin + '/api/tickets', init);
  } catch (e) {
    return down();
  }
  const ct = res.headers.get('content-type');
  // tunnel/Pi mati -> Cloudflare membalas halaman error (5xx, bukan JSON)
  if (res.status >= 500 && !(ct || '').includes('json')) return down();
  const out = new Headers({ 'cache-control': 'no-store' });
  if (ct) out.set('content-type', ct);
  return new Response(res.body, { status: res.status, headers: out });
}
