"""Tulis llms.txt (profil perusahaan ringkas untuk asisten AI) dan llms-full.txt (versi lengkap: FAQ, proyek, halaman).
Semua fakta diambil dari site_data.py dan portofolio_data.py supaya sama dengan situs dan schema. Jalankan lewat build_all.sh."""
import html, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from site_data import SITE, OFFICES, PHONE_DISPLAY, EMAIL, FACTS, SAME_AS, HOME_FAQ, with_city
from portofolio_data import PROJECTS, CLIENT_NAMES

root = pathlib.Path(__file__).resolve().parent.parent


def title_of(path):
    f = root / (path.strip('/') + '.html')
    if not f.exists():
        return ''
    m = re.search(r'<title>([^<]*)</title>', f.read_text(encoding='utf-8'))
    return html.unescape(m.group(1)).split(' | ')[0].strip() if m else ''


def sitemap_urls():
    return re.findall(r'<loc>https://altora\.id([^<]*)</loc>', (root / 'sitemap.xml').read_text(encoding='utf-8'))


offices = '\n'.join(f"- {o['label']}: {with_city(o)}, {o['region']}, Indonesia" for o in OFFICES)
same_as = '\n'.join(f'- {u}' for u in SAME_AS) or '- (belum ada profil eksternal resmi yang dicantumkan)'
KEY_PROJECTS = ['cctv-ai-farmasi-unmul', 'smart-attendance-unmul', 'website-feb-unmul', 'deteksi-apd-ai', 'hris-mobile-payroll',
                'fleet-management-tambang', 'optimasi-rute-armada', 'pompy-batara', 'fleet-radio-kapal', 'antrian-poliklinik']
BY = {p['slug']: p for p in PROJECTS}


def proj_line(p):
    return f"- {p['title']} — {p['client']}{' (' + p['year'] + ')' if p['year'] else ''}: {SITE}/portofolio/{p['slug']}"


PROFILE = f"""# Altora Indonesia

> Altora Indonesia (Altora) adalah software house yang berkantor pusat di Samarinda, Kalimantan Timur, Indonesia, sejak {FACTS['since']}, dengan dua kantor cabang di Balikpapan. Altora membuat software custom, aplikasi web dan mobile, website, SEO, AI, dan IoT, serta menyediakan pengadaan dan pemasangan perangkat untuk perusahaan dan instansi di Kalimantan Timur.

Altora Indonesia (Altora) is a software house headquartered in Samarinda, East Kalimantan (Kalimantan Timur), Indonesia, founded in {FACTS['since']}, with two branch offices in Balikpapan. Not related to other companies named "Altora" outside Indonesia.

## Fakta utama
- Nama: Altora Indonesia (nama pendek: Altora; nama lama: Algora Teknologi Indonesia)
- Situs resmi: {SITE}/
- Berdiri: {FACTS['since']}, di Samarinda
- Pengalaman: {FACTS['years']} tahun, {FACTS['projects']} proyek terdeliver, {FACTS['team']} ahli in-house
- Legalitas: berstatus PKP, terdaftar sebagai penyedia di Inaproc/LKPP (pengadaan pemerintah)
- Telepon/WhatsApp: {PHONE_DISPLAY} (https://wa.me/6285190911170)
- Email: {EMAIL}

## Kantor
{offices}
- Peta kantor pusat: https://www.google.com/maps?q=-0.5810649,117.2105898 (perkiraan titik Kelurahan Bukuan, Palaran)

## Layanan
- Software custom, aplikasi web, dan aplikasi mobile (Android/iOS): {SITE}/services/software-custom
- Pembuatan website dan SEO: {SITE}/services/website-seo, {SITE}/services/seo
- AI (analitik CCTV, deteksi APD, pengenalan wajah) dan IoT (sensor): {SITE}/services/ai-custom, {SITE}/services/iot-custom
- Tracking armada dan aset: {SITE}/services/tracking
- Pengadaan dan pemasangan perangkat untuk perusahaan dan instansi di Kalimantan Timur (CCTV VIGI dan Dahua, jaringan, server rack, GPS Teltonika, videotron, laptop/PC Lenovo): {SITE}/pengadaan
- Kit Starlink dan pemasangannya, khusus wilayah Kalimantan Timur. Altora bukan mitra resmi Starlink.
- Khusus Samarinda: pasang CCTV rumahan, smart lock, smart home, IT support bulanan
- Tanpa daftar harga publik; penawaran tertulis lewat WhatsApp

## Area layanan
- Langsung dari kantor: Samarinda, Balikpapan
- Dari kantor terdekat: Bontang, Kutai Kartanegara, Kutai Timur, Kutai Barat, Mahakam Ulu, Berau, Paser, Penajam Paser Utara, IKN Nusantara
- Software dan website juga dikerjakan jarak jauh untuk klien di seluruh Indonesia

## Klien dan proyek nyata
- Klien antara lain: {', '.join(CLIENT_NAMES)}
{chr(10).join(proj_line(BY[s]) for s in KEY_PROJECTS if s in BY)}

## Halaman penting
- Software house Samarinda: {SITE}/software-house-samarinda
- Software house Balikpapan: {SITE}/software-house-balikpapan
- Software house Kalimantan Timur: {SITE}/software-house-kalimantan-timur
- Jasa pembuatan aplikasi Samarinda: {SITE}/jasa-pembuatan-aplikasi-samarinda
- Jasa pembuatan aplikasi Balikpapan: {SITE}/jasa-pembuatan-aplikasi-balikpapan
- Jasa pembuatan website Samarinda: {SITE}/jasa-pembuatan-website-samarinda
- Tentang Altora: {SITE}/about
- Kontak: {SITE}/contact
- Layanan: {SITE}/services
- Pengadaan perangkat: {SITE}/pengadaan
- Portofolio: {SITE}/portofolio
- Aplikasi buatan Altora (Altora Office, Teams, Store, FieldOps, Control Center): {SITE}/aplikasi
- Area layanan: {SITE}/area-layanan
- Artikel: {SITE}/blog
- Versi lengkap untuk AI: {SITE}/llms-full.txt

## Profil resmi di luar situs (sameAs)
{same_as}
"""


def full():
    faq = '\n\n'.join(f'### {q}\n{a}' for q, a in HOME_FAQ)
    projects = '\n'.join(proj_line(p) + f"\n  {p['desc']}" for p in PROJECTS)
    urls = sitemap_urls()
    def section(pred):
        return '\n'.join(f'- {title_of(u) or u}: {SITE}{u}' for u in urls if pred(u))
    return (PROFILE.replace('- Versi lengkap untuk AI: ' + SITE + '/llms-full.txt\n', '')
            + f"\n## Pertanyaan umum\n\n{faq}\n\n## Semua proyek portofolio\n{projects}\n"
            + "\n## Halaman layanan\n" + section(lambda u: u.startswith('/services/') or u in ('/pengadaan', '/infrastruktur-hardware-kaltim'))
            + "\n\n## Halaman kota (Kalimantan)\n" + section(lambda u: re.match(r'/(software-house|jasa-|it-support|jual-|cctv-)', u) is not None)
            + "\n\n## Aplikasi buatan Altora\n" + section(lambda u: u.startswith('/aplikasi'))
            + "\n\n## Artikel\n" + section(lambda u: u.startswith('/blog/')) + '\n')


if __name__ == '__main__':
    (root / 'llms.txt').write_text(PROFILE, encoding='utf-8')
    (root / 'llms-full.txt').write_text(full(), encoding='utf-8')
    print('llms.txt dan llms-full.txt ditulis')
