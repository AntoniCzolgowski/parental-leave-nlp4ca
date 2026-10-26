"""OpenAlex pulls for the feasibility test (institutions for twin matching, random author samples).
API key: environment variable OPENALEX_KEY (never commit it).
Usage: python3 src/01_pull_openalex.py authors|movers|inst_us|inst_eu   (resumable)"""
import os, sys, json, time, urllib.request, urllib.parse
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / 'data' / 'openalex'; OUT.mkdir(parents=True, exist_ok=True)
KEY = os.environ.get('OPENALEX_KEY', '')
EU = 'GB|DE|FR|NL|CH|SE|DK|NO|FI|BE|AT|IT|ES|PT|IE|PL|CZ'
SEL_A = 'id,display_name,works_count,cited_by_count,affiliations,last_known_institutions'
SEL_I = 'id,display_name,country_code,type,works_count,cited_by_count,summary_stats,topics,geo,ror,homepage_url'

def get(base, params, tries=6):
    if KEY: params = dict(params, api_key=KEY)
    url = base + '?' + urllib.parse.urlencode(params, safe=':|,')
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read())
        except Exception:
            time.sleep(2 * (k + 1))
    raise RuntimeError('failed ' + str(params.get('filter'))[:60])

def sample_pages(tag, flt, seeds, sel, base='https://api.openalex.org/authors'):
    for seed in seeds:
        for page in range(1, 51):  # 50 x 200 = 10,000, the OpenAlex maximum sample
            f = OUT / f'{tag}_s{seed}_p{page:02d}.json'
            if f.exists(): continue
            d = get(base, {'filter': flt, 'sample': 10000, 'seed': seed, 'per-page': 200, 'page': page, 'select': sel})
            f.write_text(json.dumps(d['results']))
            if not d['results']: break

def top_institutions(tag, flt, n_pages):
    for page in range(1, n_pages + 1):
        f = OUT / f'{tag}_p{page:02d}.json'
        if f.exists(): continue
        d = get('https://api.openalex.org/institutions', {'filter': flt, 'sort': 'works_count:desc', 'per-page': 200, 'page': page, 'select': SEL_I})
        f.write_text(json.dumps(d['results']))

what = sys.argv[1]
if what == 'authors':   # population at risk: ever US-affiliated, 10-1000 works
    sample_pages('pop', 'affiliations.institution.country_code:US,works_count:10-1000', [11, 22, 33], SEL_A)
elif what == 'movers':  # boost sample: ever US-affiliated and last known in Europe
    sample_pages('mov', 'affiliations.institution.country_code:US,last_known_institutions.country_code:' + EU + ',works_count:10-1000', [44], SEL_A)
elif what == 'inst_us':
    top_institutions('inst_us', 'country_code:US,type:education', 1)
elif what == 'inst_eu':
    top_institutions('inst_eu', 'country_code:' + EU + ',type:education', 3)
print('done', what)
