import pandas as pd, numpy as np
EU=set('GB DE FR NL CH SE DK NO FI BE AT IT ES PT IE PL CZ'.split())
df=pd.read_pickle('data/mob.pkl')
df=df[(df.start>=1990)&(df.start<=2018)&df.gender.isin(['W','M'])].copy()
df['orig']=df.apply(lambda r: 'US' if 'US' in r.yc[r.start] else ('EU' if r.yc[r.start]&EU else 'OTH'),axis=1)
bins=[-1,2,5,8,11,14,19,60]; labs=['0-2','3-5','6-8','9-11','12-14','15-19','20+']
pop=df[df.s=='pop']
recs=[]
for r in pop.itertuples():
    exitflag = (r.dest=='STAY_OR_EXIT') and (r.end==r.L) and (r.L<=2020)
    for y in r.us:
        if y>r.L or y<2000 or y>2020: continue
        last = (y==r.L)
        recs.append((r.id,r.gender,r.orig,y-r.start, int(last and r.dest=='EU'), int(last and r.dest=='OTHER'), int(last and exitflag)))
py=pd.DataFrame(recs,columns=['id','g','orig','ca','eu','oth','exit']); py['cab']=pd.cut(py.ca,bins,labels=labs)
rng=np.random.default_rng(7)
ids=py.id.unique()
def rr(d,ev):
    a=d.groupby(['cab','g'],observed=True)[ev].agg(['sum','size']).unstack('g')
    return (a[('sum','W')]/a[('size','W')])/(a[('sum','M')]/a[('size','M')])
res={}
for ev in ['eu','oth','exit']:
    est=rr(py,ev)
    # cluster bootstrap over authors
    g=py.groupby('id')
    bs=[]
    for b in range(300):
        samp=rng.choice(ids,len(ids),replace=True)
        cnt=pd.Series(samp).value_counts()
        d=py.merge(cnt.rename('w'),left_on='id',right_index=True)
        a=d.assign(e=d[ev]*d.w).groupby(['cab','g'],observed=True).agg(s=('e','sum'),n=('w','sum')).unstack('g')
        bs.append((a[('s','W')]/a[('n','W')])/(a[('s','M')]/a[('n','M')]))
    B=pd.concat(bs,axis=1)
    res[ev]=pd.DataFrame({'RR':est,'lo':B.quantile(.025,axis=1),'hi':B.quantile(.975,axis=1)})
    print(ev, 'events W/M:', py[py.g=='W'][ev].sum(), py[py.g=='M'][ev].sum()); print(res[ev].round(2))
pd.concat(res,axis=1).to_csv('outputs/rr_dest.csv')
