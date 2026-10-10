from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import quote
import re, time, requests, html as htmlmod

ROOT=Path('.')
EXCLUDE={'google34eeef0a0519ad2c.html','login.html'}
files=[p for p in ROOT.rglob('*.html') if '.git' not in p.parts and p.name not in EXCLUDE and not (p.parts and p.parts[0]=='id')]
cache={}
keep_terms=['Altora','ALTORA','AI','IoT','CCTV','SEO','HRIS','KPI','CMS','DAPODIK','UNMUL','Balikpapan','Samarinda','Indonesia','WhatsApp','Google','Cloudflare','Fleet Management','Command Center','AI Vision','Software Custom','Website','Projects','Project']

def translate_one(text):
    text=text.strip()
    if not text or len(text)<2 or text in cache: return cache.get(text,text)
    # protect identifiers, URLs and brand terms
    protected={}
    x=text
    for i, term in enumerate(sorted(keep_terms,key=len,reverse=True)):
        key=f'ZXTERM{i}Q'
        if term in x: x=x.replace(term,key); protected[key]=term
    try:
        data=requests.get('https://api.mymemory.translated.net/get',params={'q':x,'langpair':'id|en'},timeout=18).json()
        out=data.get('responseData',{}).get('translatedText','')
        if not out or data.get('responseStatus') != 200: out=x
    except Exception: out=x
    out=htmlmod.unescape(out)
    for key,term in protected.items(): out=out.replace(key,term)
    cache[text]=out
    time.sleep(.17)
    return out

def process_texts(soup):
    skip={'script','style','svg','code','pre'}
    attrs=['placeholder','title','aria-label','alt']
    for node in list(soup.find_all(string=True)):
        parent=node.parent
        if not parent or parent.name in skip: continue
        raw=str(node)
        if raw.strip() and re.search(r'[A-Za-zÀ-ÿ]',raw) and not re.fullmatch(r'[\s\d•·→↗↓★✦✕×—–|.,:;!?()\[\]{}+\-_/&%#@]+',raw):
            lead=re.match(r'^\s*',raw).group(0); tail=re.search(r'\s*$',raw).group(0)
            node.replace_with(lead+translate_one(raw.strip())+tail)
    for tag in soup.find_all(True):
        for a in attrs:
            if tag.has_attr(a) and re.search(r'[A-Za-zÀ-ÿ]',tag[a]): tag[a]=translate_one(tag[a])

def route_for(p,lang):
    rel=p.relative_to(ROOT).with_suffix('')
    if rel.name=='index': return '/' if lang=='en' else '/id/'
    return '/'+('/'.join(rel.parts) if lang=='en' else 'id/'+'/'.join(rel.parts))

def normalize_link(v,from_id=False):
    if not v or v.startswith(('#','mailto:','tel:','https:','http:','javascript:')): return v
    if v.startswith('/assets/') or v.startswith('assets/'): return v
    frag=''
    if '#' in v: v,frag=v.split('#',1); frag='#'+frag
    if not v: return frag
    v=v.replace('.html','').rstrip('/')
    if from_id:
      if v.startswith('/'): return '/id'+(v if v!='/' else '/')+frag
      return '/id/'+v.lstrip('./')+frag
    return v+frag

for p in files:
    raw=p.read_text(encoding='utf-8')
    soup=BeautifulSoup(raw,'html.parser')
    # Existing Indonesian originals become /id copies
    soup.html['lang']='id'
    head=soup.head
    for tag in head.select('link[rel="alternate"][hreflang]'): tag.decompose()
    base_id='https://altora.id'+route_for(p,'id')
    base_en='https://altora.id'+route_for(p,'en')
    canon=head.find('link',rel='canonical')
    if canon: canon['href']=base_id
    else: head.append(soup.new_tag('link',rel='canonical',href=base_id))
    for lang,url in [('en',base_en),('id',base_id),('x-default',base_en)]: head.append(soup.new_tag('link',rel='alternate',hreflang=lang,href=url))
    for a in soup.find_all('a',href=True): a['href']=normalize_link(a['href'],True)
    dest=ROOT/'id'/p.relative_to(ROOT); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(str(soup),encoding='utf-8')

    # English clone from original source
    en=BeautifulSoup(raw,'html.parser'); en.html['lang']='en'
    process_texts(en)
    h=en.head
    for tag in h.select('link[rel="alternate"][hreflang]'): tag.decompose()
    canon=h.find('link',rel='canonical')
    if canon: canon['href']=base_en
    else: h.append(en.new_tag('link',rel='canonical',href=base_en))
    for lang,url in [('en',base_en),('id',base_id),('x-default',base_en)]: h.append(en.new_tag('link',rel='alternate',hreflang=lang,href=url))
    for a in en.find_all('a',href=True): a['href']=normalize_link(a['href'],False)
    # Add translation client and language switch asset in every document
    b=en.body
    if b: b.append(en.new_tag('script',src='/assets/js/locale-switcher.js?v=20260922-v1',defer='defer'))
    p.write_text(str(en),encoding='utf-8')
print(f'localized {len(files)} pages; Indonesian copies in id/')
