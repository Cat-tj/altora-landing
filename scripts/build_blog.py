"""Bangun blog dari content/blog/*.md -> blog.html (daftar) + blog/<slug>.html, lalu perbarui sitemap.xml.

Format artikel (front matter sederhana, satu kunci per baris):
    ---
    title: Judul artikel
    description: Ringkasan 120-160 karakter untuk Google
    date: 2026-10-11
    updated: 2026-10-11          (opsional)
    category: Panduan
    image: /assets/img/produk/vision.webp   (opsional, untuk kartu & preview link)
    related: /produk#attendance | Altora Smart Attendance   (opsional, boleh lebih dari satu baris related)
    ---
    Isi Markdown: ## / ### heading, paragraf, - list, 1. list, **tebal**, *miring*, [teks](url), `kode`, > kutipan

Jalankan dari root repo:  python3 scripts/build_blog.py && python3 scripts/apply_shell.py
Artikel yang namanya diawali "_" dianggap draf dan tidak dipublikasikan.
"""
import datetime, html, json, pathlib, re
from urllib.parse import quote

root = pathlib.Path(__file__).resolve().parent.parent
SRC = root / 'content/blog'
OUT = root / 'blog'
SITE = 'https://altora.id'
CSS_VER = '20261012d'
BULAN = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

e = lambda t: html.escape(t, quote=True)


def tanggal(iso):
    d = datetime.date.fromisoformat(iso)
    return f'{d.day} {BULAN[d.month - 1]} {d.year}'


def parse(path):
    raw = path.read_text(encoding='utf-8')
    m = re.match(r'---\n(.*?)\n---\n(.*)', raw, re.S)
    if not m:
        raise SystemExit(f'{path.name}: front matter tidak ditemukan')
    meta, related = {}, []
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        k, _, v = line.partition(':')
        k, v = k.strip(), v.strip()
        if k == 'related':
            url, _, label = v.partition('|')
            related.append((url.strip(), label.strip()))
        else:
            meta[k] = v
    for k in ('title', 'description', 'date', 'category'):
        if k not in meta:
            raise SystemExit(f'{path.name}: kunci "{k}" wajib diisi')
    meta['slug'] = path.stem
    meta['related'] = related
    meta['body_md'] = m.group(2).strip()
    return meta


def inline(t):
    t = e(t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)', r'<em>\1</em>', t)

    def link(mo):
        label, url = mo.group(1), html.unescape(mo.group(2))
        ext = url.startswith('http') and not url.startswith(SITE)
        attrs = ' rel="noopener" target="_blank"' if ext else ''
        return f'<a href="{e(url)}"{attrs}>{label}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link, t)


def md_to_html(md):
    out, toc, para, items, kind = [], [], [], [], None

    def flush():
        nonlocal para, items, kind
        if para:
            out.append(f'<p>{inline(" ".join(para))}</p>')
            para = []
        if items:
            out.append(f'<{kind}>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + f'</{kind}>')
            items, kind = [], None

    for line in md.splitlines():
        s = line.rstrip()
        if not s.strip():
            flush(); continue
        h = re.match(r'(#{2,3})\s+(.*)', s)
        if h:
            flush()
            level, text = len(h.group(1)), h.group(2).strip()
            hid = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            if level == 2:
                toc.append((hid, text))
            out.append(f'<h{level} id="{hid}">{inline(text)}</h{level}>')
            continue
        if s.startswith('> '):
            flush(); out.append(f'<blockquote><p>{inline(s[2:])}</p></blockquote>'); continue
        li = re.match(r'\s*(?:-|\*)\s+(.*)', s)
        ol = re.match(r'\s*\d+\.\s+(.*)', s)
        if li or ol:
            want = 'ul' if li else 'ol'
            if para or (kind and kind != want):
                flush()
            kind = want
            items.append((li or ol).group(1))
            continue
        if items:
            flush()
        para.append(s.strip())
    flush()
    return '\n'.join(out), toc


def head(title, desc, canonical, og_type='website', image=None, extra=''):
    img = SITE + (image or '/assets/img/produk/vision.webp')
    return (f'<!DOCTYPE html>\n<html lang="id"><head><meta charset="utf-8"/><meta content="width=device-width,initial-scale=1" name="viewport"/>'
            f'<title>{e(title)}</title><meta content="{e(desc)}" name="description"/><link href="{SITE}{canonical}" rel="canonical"/>'
            f'<meta content="id_ID" property="og:locale"/><meta content="{og_type}" property="og:type"/><meta content="{e(title)}" property="og:title"/>'
            f'<meta content="{e(desc)}" property="og:description"/><meta content="{SITE}{canonical}" property="og:url"/><meta content="{img}" property="og:image"/>'
            '<link href="/assets/img/altora-logo-icon-v2.svg" rel="icon"/><link href="https://fonts.googleapis.com" rel="preconnect"/><link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>'
            '<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet"/>'
            '<link href="/assets/css/styles.css?v=20260920-company-pages" rel="stylesheet"/><link href="/assets/css/company-pages.css?v=20260920-company-pages" rel="stylesheet"/>'
            '<link href="/assets/css/shared-shell.css?v=20260920-shared-shell" rel="stylesheet"/><link href="/assets/css/site-shell.css?v=20260922-white-frost-v7" rel="stylesheet"/>'
            f'<link rel="stylesheet" href="/assets/css/unify.css?v={CSS_VER}"/>{extra}</head><body class="company-page"><header></header>\n')


TAIL = '<footer></footer>\n<script defer="" src="/assets/js/site-shell.js?v=20261010e"></script></body></html>\n'
WA = 'https://wa.me/6285190911170?text='


def build():
    posts = [parse(p) for p in sorted(SRC.glob('*.md')) if not p.name.startswith('_')]
    posts.sort(key=lambda p: p['date'], reverse=True)
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob('*.html'):
        if old.stem not in {p['slug'] for p in posts}:
            old.unlink()

    for p in posts:
        body, toc = md_to_html(p['body_md'])
        words = len(re.sub(r'<[^>]+>', ' ', body).split())
        minutes = max(1, round(words / 200))
        url = f'/blog/{p["slug"]}'
        updated = p.get('updated', p['date'])
        ld = {'@context': 'https://schema.org', '@graph': [
            {'@type': 'BlogPosting', 'headline': p['title'], 'description': p['description'], 'datePublished': p['date'],
             'dateModified': updated, 'inLanguage': 'id-ID', 'mainEntityOfPage': SITE + url,
             'image': SITE + p.get('image', '/assets/img/produk/vision.webp'),
             'author': {'@type': 'Organization', 'name': 'Tim Altora Indonesia', 'url': SITE + '/'},
             'publisher': {'@type': 'Organization', 'name': 'Altora Indonesia', 'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/img/altora-logo-icon-v2.svg'}}},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Beranda', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Artikel', 'item': SITE + '/blog'},
                {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': SITE + url}]}]}
        toc_html = ''
        if len(toc) >= 3:
            toc_html = ('<nav aria-label="Daftar isi" class="bl-toc"><b>Daftar isi</b><ol>'
                        + ''.join(f'<li><a href="#{i}">{e(t)}</a></li>' for i, t in toc) + '</ol></nav>')
        related = ''
        if p['related']:
            related = ('<aside class="bl-related"><b>Terkait di Altora</b>'
                       + ''.join(f'<a href="{e(u)}">{e(l)} →</a>' for u, l in p['related']) + '</aside>')
        others = [o for o in posts if o['slug'] != p['slug']][:3]
        more = ''
        if others:
            more = ('<section class="bl-more"><div class="bl-wrap"><h2>Artikel lainnya</h2><div class="bl-grid">'
                    + ''.join(card(o) for o in others) + '</div></div></section>')
        msg = f'Halo Altora, saya baru membaca artikel "{p["title"]}" dan ingin berdiskusi.'
        page = (head(f'{p["title"]} | Altora Indonesia', p['description'], url, 'article', p.get('image'),
                     f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
                + '<main class="bl-page">'
                + '<article class="bl-article"><header class="bl-head"><div class="bl-wrap bl-narrow">'
                + '<nav aria-label="Breadcrumb" class="bl-crumb"><a href="/">Beranda</a><span>/</span><a href="/blog">Artikel</a></nav>'
                + f'<p class="eyebrow eyebrow-purple">{e(p["category"])}</p><h1>{e(p["title"])}</h1>'
                + f'<p class="bl-lead">{e(p["description"])}</p>'
                + f'<p class="bl-meta">Tim Altora Indonesia · <time datetime="{p["date"]}">{tanggal(p["date"])}</time> · {minutes} menit baca</p>'
                + '</div></header>'
                + f'<div class="bl-wrap bl-narrow bl-body">{toc_html}{body}{related}'
                + '<div class="bl-cta"><div><b>Punya kondisi serupa di organisasi Anda?</b><p>Ceritakan prosesnya. Kami bantu memetakan pendekatan yang paling proporsional.</p></div>'
                + f'<a class="btn btn-purple" href="{WA}{quote(msg)}" rel="noopener" target="_blank">Diskusi via WhatsApp →</a></div>'
                + '</div></article>' + more + '</main>\n' + TAIL)
        (OUT / f'{p["slug"]}.html').write_text(page, encoding='utf-8')

    index_ld = {'@context': 'https://schema.org', '@type': 'Blog', 'name': 'Artikel Altora Indonesia', 'url': SITE + '/blog',
                'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': f'{SITE}/blog/{p["slug"]}', 'datePublished': p['date']} for p in posts]}
    index = (head('Artikel Altora | Panduan Software, Aplikasi, AI CCTV & IoT', 'Panduan praktis dari tim Altora Indonesia tentang software, aplikasi, website, AI CCTV, dan IoT untuk bisnis dan organisasi di Balikpapan, Samarinda, dan Indonesia.',
                  '/blog', extra=f'<script type="application/ld+json">{json.dumps(index_ld, ensure_ascii=False)}</script>')
             + '<main class="bl-page"><section class="bl-index-head"><div class="bl-wrap">'
             + '<p class="eyebrow eyebrow-purple">Artikel</p><h1>Panduan praktis untuk merapikan operasional dengan teknologi.</h1>'
             + '<p class="bl-lead">Tulisan tim Altora tentang software, aplikasi, website, AI CCTV, dan IoT—ditulis untuk pemilik usaha dan pengelola organisasi, bukan untuk programmer.</p>'
             + '</div></section><section class="bl-list"><div class="bl-wrap"><div class="bl-grid">'
             + ''.join(card(p) for p in posts) + '</div></div></section></main>\n' + TAIL)
    (root / 'blog.html').write_text(index, encoding='utf-8')

    update_sitemap(posts)
    print(f'blog: {len(posts)} artikel dibangun')


def card(p):
    img = p.get('image')
    pic = f'<div class="bl-card-img"><img alt="" loading="lazy" src="{e(img)}"/></div>' if img else ''
    return (f'<a class="bl-card" href="/blog/{p["slug"]}">{pic}<div class="bl-card-body"><small>{e(p["category"])} · {tanggal(p["date"])}</small>'
            f'<h3>{e(p["title"])}</h3><p>{e(p["description"])}</p><span>Baca artikel →</span></div></a>')


def update_sitemap(posts):
    sm = root / 'sitemap.xml'
    s = sm.read_text(encoding='utf-8')
    s = re.sub(r'  <url><loc>https://altora\.id/blog[^<]*</loc>.*?</url>\n', '', s)
    newest = posts[0].get('updated', posts[0]['date']) if posts else datetime.date.today().isoformat()
    rows = [f'  <url><loc>{SITE}/blog</loc><lastmod>{newest}</lastmod><priority>0.7</priority></url>']
    rows += [f'  <url><loc>{SITE}/blog/{p["slug"]}</loc><lastmod>{p.get("updated", p["date"])}</lastmod><priority>0.6</priority></url>' for p in posts]
    s = s.replace('</urlset>', '\n'.join(rows) + '\n</urlset>')
    sm.write_text(s, encoding='utf-8')


if __name__ == '__main__':
    build()
