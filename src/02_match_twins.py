import json, math, random, collections, numpy as np, pandas as pd
D='data/openalex/'
us=json.load(open(D+'inst_us_p01.json'))
eu=sum([json.load(open(D+f'inst_eu_p0{i}.json')) for i in (1,2,3)],[])
BAD=['Medic','Health','Hospital','Clinic','Icahn','Baylor College','San Francisco','System','Cancer','Mayo','Weill','Charité','Sorbonne Université','Assistance Publique','Inserm','CNRS','Max Planck','Helmholtz','Fraunhofer','Pierre-et-Marie-Curie','Paris Diderot','Paris-Sud','Paris Descartes','Université Paris-Saclay ','Paris Sciences et Lettres']
def ok(r): return not any(b.lower() in r['display_name'].lower() for b in BAD)
fields=sorted({t['field']['display_name'] for r in us+eu for t in r['topics']})
def vec(r):
    v=collections.Counter()
    for t in r['topics']: v[t['field']['display_name']]+=t['count']
    a=np.array([v[f] for f in fields],float); return a/max(a.sum(),1)
def feats(r):
    return vec(r), math.log(r['works_count']), math.log(r['cited_by_count']/r['works_count'])
PFL={'California','New Jersey','Rhode Island','New York','Washington','Massachusetts','Connecticut','Oregon','Colorado','District of Columbia'}
U=[r for r in us if ok(r)][:80]
pfl=[r for r in U if r['geo']['region'] in PFL]; non=[r for r in U if r['geo']['region'] not in PFL]
random.seed(2026)
cu=[r for r in U if r['display_name']=='University of Colorado Boulder'][0]
pfl_s=[cu]+random.sample([r for r in pfl if r is not cu],9); non_s=random.sample(non,10)
S=pfl_s+non_s
E=[r for r in eu if ok(r)]
F={r['id']:feats(r) for r in S+E}
def dist(a,b):
    va,wa,ca=F[a['id']]; vb,wb,cb=F[b['id']]
    cos=1-va@vb/(np.linalg.norm(va)*np.linalg.norm(vb))
    return cos + 0.5*abs(wa-wb) + 0.5*abs(ca-cb)
from scipy.optimize import linear_sum_assignment
M=np.array([[dist(a,b) for b in E] for a in S])
pen=np.zeros_like(M)
for it in range(50):
    r,c=linear_sum_assignment(M+pen)
    cnt=collections.Counter(E[j]['country_code'] for j in c)
    over=[k for k,v in cnt.items() if v>4]
    if not over: break
    for k in over:
        rows_k=[(M[i,j],i) for i,j in zip(r,c) if E[j]['country_code']==k]
        _,iw=max(rows_k)
        for j,b in enumerate(E):
            if b['country_code']==k: pen[iw,j]+=10
match={i:(j,M[i,j]) for i,j in zip(r,c)}
cap=collections.Counter(E[j]['country_code'] for j in c)
rows=[]
for i,a in enumerate(S):
    j,d=match[i]; b=E[j]
    rows.append(dict(us=a['display_name'],state=a['geo']['region'],pfl=a['geo']['region'] in PFL,us_works=a['works_count'],us_cpp=round(a['cited_by_count']/a['works_count'],1),us_home=a.get('homepage_url'),
                     eu=b['display_name'],country=b['country_code'],eu_works=b['works_count'],eu_cpp=round(b['cited_by_count']/b['works_count'],1),eu_home=b.get('homepage_url'),dist=round(d,3),us_id=a['id'],eu_id=b['id']))
df=pd.DataFrame(rows); df.to_csv('outputs/twins.csv',index=False)
pd.set_option('display.width',250); print(df[['us','state','pfl','us_works','us_cpp','eu','country','eu_works','eu_cpp','dist']].to_string())
print(cap)
