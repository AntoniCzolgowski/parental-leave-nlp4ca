"""Figure A1: categorical policy fields by continent (counts out of 20)."""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in ['regular','bold']: fm.fontManager.addfont(f'/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-{f}.otf')
plt.rcParams.update({'font.family':'TeX Gyre Termes','font.size':8,'pdf.fonttype':42})
d=pd.read_csv('outputs/all_fields_40.csv')
S=['#2a78d6','#eb6834','#1baf7a','#eda100']; GRAY='#c9c8c3'; INK='#0b0b0b'; MUTED='#52514e'
def tr(v):
    if pd.isna(v): return 'not stated'
    return 'none' if v==0 else ('half' if v==0.5 else 'one or more')
panels=[
 ('Framing','framing',[('neutral','neutral'),('mixed','mixed'),('gendered','gendered')]),
 ('Caregiver clause','primary_caregiver_clause',[(True,'yes'),(False,'no')]),
 ('Tenure clock','tenure_clock',[('automatic','automatic'),('on_request','on request'),('not_applicable','no tenure track')]),
 ('Teaching relief','tr',[('one or more','1+ semester'),('half','half'),('none','none')]),
 ('Who pays','payer',[('university','university'),('state_or_insurance','state/insurance'),('mixed','mixed')]),
]
d['tr']=d.teaching_relief_semesters.map(tr)
fig,axes=plt.subplots(1,5,figsize=(7.0,1.75),gridspec_kw={'wspace':0.12})
for ax,(title,col,cats) in zip(axes,panels):
    for row,side,lab in [(1,'US','US'),(0,'EU','Europe')]:
        sub=d[d.side==side][col]
        left=0
        vals=[(c,lb,int((sub==c).sum())) for c,lb in cats]
        ns=20-sum(v for _,_,v in vals)
        for i,(c,lb,v) in enumerate(vals):
            if v: 
                ax.barh(row,v,left=left,color=S[i],height=0.62,edgecolor='white',linewidth=1.2)
                if v>=2: ax.text(left+v/2,row,str(v),ha='center',va='center',color='white',fontsize=7.5,fontweight='bold')
            left+=v
        if ns: ax.barh(row,ns,left=left,color=GRAY,height=0.62,edgecolor='white',linewidth=1.2)
    ax.set_xlim(0,20); ax.set_ylim(-0.6,1.6); ax.set_xticks([]); ax.set_title(title,fontsize=8.3,loc='left',color=INK)
    ax.set_yticks([0,1]); ax.set_yticklabels(['Europe','US'] if ax is axes[0] else ['',''],fontsize=7.8,color=MUTED)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
    # legend under panel
    handles=[plt.Rectangle((0,0),1,1,color=S[i]) for i in range(len(cats))]+[plt.Rectangle((0,0),1,1,color=GRAY)]
    labels=[lb for _,lb in cats]+['not stated']
    ax.legend(handles,labels,loc='upper left',bbox_to_anchor=(0,-0.02),frameon=False,fontsize=6.6,handlelength=0.9,handleheight=0.9,ncol=1,labelspacing=0.2,borderaxespad=0)
fig.savefig('proposal/figA1.pdf',bbox_inches='tight',pad_inches=0.02); fig.savefig('outputs/figA1.png',dpi=200,bbox_inches='tight',pad_inches=0.02)
print('ok')
