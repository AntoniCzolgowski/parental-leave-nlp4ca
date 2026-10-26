import pandas as pd, numpy as np, json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in ['/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-regular.otf','/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-bold.otf','/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-italic.otf']: fm.fontManager.addfont(f)
plt.rcParams.update({'font.family':'TeX Gyre Termes','font.size':8.5,'axes.titlesize':9,'axes.labelsize':8.5,'xtick.labelsize':7.5,'ytick.labelsize':7.5,
  'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#52514e','axes.linewidth':0.6,'xtick.color':'#52514e','ytick.color':'#52514e','axes.labelcolor':'#0b0b0b','pdf.fonttype':42})
BLUE,ORANGE,AQUA,INK,MUTED='#2a78d6','#eb6834','#1baf7a','#0b0b0b','#8a8984'
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7.0,1.85),gridspec_kw={'width_ratios':[1,1.3],'wspace':0.25})
# ---- panel a: strip plot by continent, two measures
import os
if os.path.exists('outputs/panel_a_all.csv'):
    p=pd.read_csv('outputs/policy_fields_by_pair.csv')
    rng=np.random.default_rng(3)
    groups=[('us_w','US',0.0,BLUE),('eu_w','Europe',0.55,ORANGE),('us_any','US',1.6,BLUE),('eu_any','Europe',2.15,ORANGE)]
    for col,lab,x0,colr in groups:
        v=p[col].dropna().values; n=len(v)
        big=v[v>62]; v=np.where(v>62,62,v)
        for bv in big: ax1.annotate(f'{bv:.0f} (Vienna)',(x0,62),xytext=(-7,0),textcoords='offset points',fontsize=6.5,color='#52514e',va='center',ha='right')
        jit=rng.uniform(-0.13,0.13,n)
        ax1.scatter(x0+jit,v,s=20,color=colr,edgecolor='white',linewidth=0.7,zorder=3,alpha=0.95)
        if n: ax1.hlines(np.median(v),x0-0.2,x0+0.2,color=INK,lw=1.6,zorder=4)
        ax1.text(x0,-6.5,f'{lab}\n{n} of 20',ha='center',va='top',fontsize=6.8,color='#52514e')
    ax1.set_xticks([]); ax1.set_xlim(-0.4,2.55); ax1.set_ylim(-1,73)
    ax1.text(0.275,72.5,'at full pay',ha='center',va='top',fontsize=7.5,color=INK)
    ax1.text(1.875,72.5,'with any pay',ha='center',va='top',fontsize=7.5,color=INK)
    ax1.set_ylabel('weeks off for a birth parent')
    ax1.set_title('(a) What the policies give, as read by the LLM',loc='left',fontsize=8.8)
    ax1.spines['bottom'].set_visible(False)
    ax1.yaxis.grid(True,color='#ecebe8',lw=0.6); ax1.set_axisbelow(True)
# ---- panel b
d=pd.read_csv('outputs/rr_dest.csv',header=[0,1],index_col=0)
x=np.arange(len(d)); labs=list(d.index)
ax2.axvspan(1.5,3.5,color='#f3f2ef',zorder=0)
ax2.text(2.5,1.83,'around first birth\n(age 33, Morgan et al.)',ha='center',va='top',fontsize=6.6,color='#52514e')
ax2.axhline(1,color='#52514e',lw=0.7,ls=(0,(3,3)),zorder=1)
for key,col,name,off in [('eu',ORANGE,'moves to Europe',-0.09),('exit',AQUA,'stops publishing (exit)',0.09)]:
    y=d[(key,'RR')].values; lo=d[(key,'lo')].values; hi=d[(key,'hi')].values
    ax2.vlines(x+off,lo,hi,color=col,lw=1.2,alpha=0.55,zorder=2)
    ax2.plot(x+off,y,color=col,lw=2,marker='o',ms=4.2,mec='white',mew=0.8,zorder=3,label=name)
ax2.set_xticks(x); ax2.set_xticklabels(labs); ax2.set_xlabel('career age (years since first affiliation)')
ax2.set_ylabel('women / men, yearly rate'); ax2.set_ylim(0.3,1.9)
ax2.set_title('(b) Who leaves US science, and where to',loc='left',fontsize=8.8)
ax2.legend(frameon=False,fontsize=7,loc='lower left',ncol=2,handlelength=1.0,borderaxespad=0.2)
ax2.yaxis.grid(True,color='#ecebe8',lw=0.6); ax2.set_axisbelow(True)
fig.savefig('proposal/fig1.pdf',bbox_inches='tight',pad_inches=0.02); fig.savefig('outputs/fig1.png',dpi=200,bbox_inches='tight',pad_inches=0.02)
print('saved')
