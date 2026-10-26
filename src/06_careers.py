"""Build author career table from OpenAlex samples: name-based gender, US spells, destination after the last US year."""
import json, re, collections, numpy as np, pandas as pd
import gender_guesser.detector as gg
det=gg.Detector(case_sensitive=False)
EU=set('GB DE FR NL CH SE DK NO FI BE AT IT ES PT IE PL CZ'.split())
rows=[]
for line in open('data/authors_compact.jsonl'):
    a=json.loads(line)
    toks=[t for t in re.split(r'[\s\-]+',a['name']) if t]
    first=toks[0] if toks else ''
    if len(first.strip('.'))<=1 or first.endswith('.') : first=''
    g=det.get_gender(first) if first else 'unknown'
    yc=collections.defaultdict(set)
    for x in a['aff']:
        for y in x['y']:
            if x['c']: yc[y].add(x['c'])
    if not yc: continue
    years=sorted(yc); start=years[0]
    us=[y for y in years if 'US' in yc[y]]
    eu=[y for y in years if yc[y]&EU]
    rows.append(dict(s=a['s'],id=a['id'],first=first,g=g,start=start,end=years[-1],us=us,eu=eu,yc=dict(yc),wc=a['wc']))
df=pd.DataFrame(rows)
print(df.s.value_counts()); print(df.g.value_counts())
def classify(r):
    us=r.us
    if len(us)<2: return None
    L=max(us)
    after=[y for y in r.eu if y>L]
    # mover: >=2 distinct European years after last US year
    if len(after)>=2: return ('EU', L, min(after))
    other=[y for y in r.yc if y>L and not ('US' in r.yc[y]) and not (r.yc[y]&EU)]
    if len(other)>=2: return ('OTHER', L, min(other))
    return ('STAY_OR_EXIT', L, None)
df['cls']=df.apply(classify,axis=1)
df=df[df.cls.notna()].copy()
df['dest']=df.cls.str[0]; df['L']=df.cls.str[1]; df['F']=df.cls.str[2]
df['gender']=df.g.map({'female':'W','male':'M','mostly_female':'W?','mostly_male':'M?'}).fillna('U')
df.to_pickle('data/mob.pkl')
pop=df[df.s=='pop']; mov=df[df.s=='mov']
print('pop authors with >=2 US years:',len(pop)); print(pop.dest.value_counts()); print(pop.gender.value_counts(normalize=True).round(3))
print('mov sample:',len(mov)); print(mov.dest.value_counts())
