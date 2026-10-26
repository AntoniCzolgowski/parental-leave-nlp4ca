import json, sys, re, subprocess, hashlib, pathlib, urllib.request
from bs4 import BeautifulSoup
OUT=pathlib.Path('data/policies'); OUT.mkdir(exist_ok=True)
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:40]
def to_text(raw, url, ctype):
    if url.lower().endswith('.pdf') or 'pdf' in ctype or raw[:4]==b'%PDF':
        p=pathlib.Path('/tmp/_x.pdf'); p.write_bytes(raw)
        return subprocess.run(['pdftotext','-layout',str(p),'-'],capture_output=True,text=True).stdout
    soup=BeautifulSoup(raw,'html.parser')
    for t in soup(['script','style','nav','header','footer','noscript','svg','form']): t.decompose()
    main=soup.find('main') or soup.find(attrs={'role':'main'}) or soup.body or soup
    txt=main.get_text('\n'); txt=re.sub(r'\n\s*\n+','\n\n',txt)
    return txt
def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (research; antoni.czolgowski@colorado.edu)'})
    with urllib.request.urlopen(req,timeout=40) as r:
        return r.read(), r.headers.get('Content-Type','')
items=json.load(open(sys.argv[1])); res=[]
for it in items:
    inst=it['institution']; urls=it.get('urls') or (it.get('university_urls',[])+it.get('national_urls',[]))
    for k,u in enumerate(urls):
        f=OUT/f"{slug(inst)}__{k}.txt"
        try:
            raw,ct=fetch(u); txt=to_text(raw,u,ct)
            f.write_text(f"URL: {u}\nINSTITUTION: {inst}\n\n"+txt)
            res.append((inst,u,'ok',len(txt.split())))
        except Exception as e:
            res.append((inst,u,'FAIL '+str(e)[:60],0))
for r in res: print(r)
