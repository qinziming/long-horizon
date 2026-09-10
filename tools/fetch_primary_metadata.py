"""Retrieve selected primary arXiv metadata without inferring experimental validity."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
import json
import re
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
IDS = '''2608.01964 2602.16313 2605.17862 2606.06324 2605.27922
2505.22954 2510.04618 2506.15841 2510.12635 2509.13313
2603.04257 2604.01664 2605.21768 2606.05885 2603.08754
2602.16165 2604.24005 2605.07725 2603.25562 2602.08234
2604.18292 2410.09024 2406.12045 2509.16941 2605.03596
2604.01212 2609.04518 2608.14380 2609.01660 2603.29231
2605.29801 2503.22738 2603.25158 2511.10395
2606.05806 2406.13352 2607.28685 2510.05244 2606.04329
2608.19303 2607.08716'''.split()

def get(identifier):
    cached = ROOT/'sources/primary_metadata'/f'{identifier}.json'
    if cached.exists():
        return json.loads(cached.read_text())
    url = 'https://arxiv.org/abs/' + identifier
    row = {'arxiv_id':identifier,'url':url,'access_date':'2026-09-10','read_level':'primary_abstract_and_metadata'}
    try:
        r = requests.get(url, timeout=40); r.raise_for_status()
        s = BeautifulSoup(r.content, 'html.parser')
        def meta(name):
            x = s.find('meta', attrs={'name':name})
            return x.get('content','') if x else ''
        abstract = s.select_one('blockquote.abstract')
        row.update(title=meta('citation_title'), first_date=meta('citation_date'),
                   current_version_date=meta('citation_online_date'),
                   abstract=abstract.get_text(' ',strip=True).removeprefix('Abstract:').strip() if abstract else '',
                   history=s.select_one('.submission-history').get_text(' ',strip=True) if s.select_one('.submission-history') else '',
                   sha256_html=hashlib.sha256(r.content).hexdigest(),status='ok')
        if not row['title'] or not row['abstract']:
            row['status']='metadata_missing'
        (ROOT/'sources/primary_metadata'/f'{identifier}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    except Exception as e:
        row.update(status='error',error=str(e))
    return row

def main():
    (ROOT/'sources/primary_metadata').mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(get, IDS))
    catalog = list(csv.DictReader((ROOT/'data/repository_catalog.csv').open()))
    for row in rows:
        row['repo_entry_ids']=[x['entry_id'] for x in catalog if x['primary_key']=='arxiv:'+row['arxiv_id']]
    (ROOT/'data/primary_evidence.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    for r in rows:
        print(r['arxiv_id'], r.get('first_date'), r.get('title'), r['status'])
        print(r.get('abstract',r.get('error','')))

if __name__=='__main__':
    main()
