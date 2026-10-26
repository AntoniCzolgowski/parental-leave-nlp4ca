import pathlib, re, collections, json
KW=re.compile(r'(parental|maternity|paternity|childbirth|child-birth|childbearing|birth|adoption|bonding|caregiver|newborn|pregnan|family leave|tenure clock|tenure-clock|probationary|stop(ping)? the clock|modified dut|teaching relief|ASMD|short-term disability|PFL|PFML|FAMLI|Mutterschutz|Elternzeit|Elterngeld|Elternschaft|Mutterschaft|Vaterschaft|Mutterschaftsurlaub|Adoptions|congé|maternité|paternité|congedo|maternit|föräldra|barsel|zwanger|ouderschap|moederschap|bevalling|permiso|nacimiento|Karenz|SMP|statutory|occupational maternity|weeks|Wochen|semaines|settimane|semanas|veckor|uger|weken)',re.I)
out=pathlib.Path('data/bundles'); out.mkdir(exist_ok=True)
groups=collections.defaultdict(list)
for f in sorted(pathlib.Path('data/policies').glob('*.txt')):
    groups[f.stem.split('__')[0]].append(f)
stats={}
for inst,files in groups.items():
    parts=[]
    for f in files:
        t=f.read_text(errors='ignore'); head,_,body=t.partition('\n\n')
        paras=[p.strip() for p in re.split(r'\n\s*\n',body) if p.strip()]
        if len(body.split())<=2500: keep=paras
        else:
            idx=set()
            for i,p in enumerate(paras):
                if KW.search(p): idx.update({i-1,i,i+1})
            keep=[paras[i] for i in sorted(idx) if 0<=i<len(paras)]
        txt='\n\n'.join(keep); w=txt.split()
        if len(w)>4000: txt=' '.join(w[:4000])+' [...truncated]'
        parts.append(f"=== SOURCE: {head.splitlines()[0]}\n{txt}")
    b='\n\n'.join(parts); (out/f'{inst}.txt').write_text(b); stats[inst]=len(b.split())
for k,v in stats.items(): print(v,k)
