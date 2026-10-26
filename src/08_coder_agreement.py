import json, pandas as pd, numpy as np, re, glob, sys
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:40]
ext={}
for f in ['outputs/extract_us.json','outputs/extract_eu_a.json','outputs/extract_eu_b.json']:
    try:
        for x in json.load(open(f)): ext[x['institution']]={k:v.get('value') for k,v in x['fields'].items()}
    except FileNotFoundError: pass
F=['birth_fullpay_weeks','nonbirth_fullpay_weeks','teaching_relief_semesters','tenure_clock','framing','primary_caregiver_clause']
def norm(k,v):
    if v is None or (isinstance(v,float) and np.isnan(v)) or v=='' : return None
    if k in F[:3]:
        try: return round(float(v),1)
        except: return None
    if k=='primary_caregiver_clause': return str(v).upper() in ('TRUE','1')
    return str(v).strip().lower()
coders={}
for f in sys.argv[1:]:
    d=pd.read_csv(f,dtype=str,keep_default_na=False)
    coders[f]={slug(r.institution):{k:norm(k,getattr(r,k)) for k in F} for r in d.itertuples()}
skip=set()
rows=[]
for name,c in coders.items():
    for inst,vals in c.items():
        key=[k for k in ext if k.startswith(inst[:30])]
        if not key or inst in skip: continue
        e=ext[key[0]]
        for k in F:
            a=norm(k,e.get(k)); b=vals[k]
            if k in F[:2] and a is not None and b is not None: ok=abs(a-b)<=1
            else: ok=(a==b)
            rows.append(dict(coder=name,inst=inst,field=k,claude=a,other=b,agree=ok))
r=pd.DataFrame(rows)
print(r.groupby(['coder','field']).agree.mean().round(2).unstack(0))
print('overall', r.groupby('coder').agree.agg(['mean','sum','size']))
print(r[~r.agree].to_string())
r.to_csv('outputs/agreement_rows.csv',index=False)
