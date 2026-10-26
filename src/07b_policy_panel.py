import json, re, pandas as pd, numpy as np
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:40]
ext={}
for f in ['outputs/extract_us.json','outputs/extract_eu_a.json','outputs/extract_eu_b.json']:
    try:
        for x in json.load(open(f)): ext[x['institution']]={k:v.get('value') for k,v in x['fields'].items()}
    except FileNotFoundError: pass
tw=pd.read_csv('outputs/twins.csv')
short={'University of Colorado Boulder':'CU Boulder','University of Kentucky':'Kentucky','University of Nottingham':'Nottingham','University of Liverpool':'Liverpool','Washington State University':'Washington St.','Université de Montpellier':'Montpellier','Florida State University':'Florida St.','Universidad Autónoma de Madrid':'UA Madrid','University of California, Los Angeles':'UCLA','University College London':'UCL'}
rows=[]
def get(name):
    k=[s for s in ext if s.startswith(slug(name)[:30])]
    return ext[k[0]] if k else {}
for r in tw.itertuples():
    a=get(r.us); b=get(r.eu)
    rows.append(dict(us=r.us,eu=r.eu,us_w=a.get('birth_fullpay_weeks'),eu_w=b.get('birth_fullpay_weeks'),us_any=a.get('birth_paid_weeks_any'),eu_any=b.get('birth_paid_weeks_any'),
                     us_non=a.get('nonbirth_fullpay_weeks'),eu_non=b.get('nonbirth_fullpay_weeks'),us_frame=a.get('framing'),eu_frame=b.get('framing'),us_pc=a.get('primary_caregiver_clause'),eu_pc=b.get('primary_caregiver_clause')))
p=pd.DataFrame(rows)
p['label']=np.where(p.us.isin(['University of Kentucky','University of Colorado Boulder','Washington State University','Florida State University']),p.us.map(lambda s: short.get(s,s)),None)
p['label_eu']=p.eu.map(lambda s: short.get(s,s))
p.to_csv('outputs/policy_fields_by_pair.csv',index=False)
both=p.dropna(subset=['us_w','eu_w'])
both.to_csv('outputs/policy_pairs_both_stated.csv',index=False)
print(p[['us','us_w','us_any','us_frame','eu','eu_w','eu_any','eu_frame']].to_string())
print('pairs with both:',len(both))
for c in ['us_w','eu_w','us_any','eu_any','us_non','eu_non']: print(c, 'n',p[c].notna().sum(),'median',p[c].median())
print('frames US',p.us_frame.value_counts().to_dict(),' EU',p.eu_frame.value_counts().to_dict())
print('paired diff (eu-us) full', (both.eu_w-both.us_w).describe().round(1).to_dict())
