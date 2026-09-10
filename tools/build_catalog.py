"""Parse the pinned README; counts describe entries, not verified publications."""
from pathlib import Path
import collections
import csv
import json
import re
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]

def canonical(url):
    m = re.search(r'arxiv.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})', url)
    if m:
        return 'arxiv:' + m[1]
    p = urlsplit(url)
    return urlunsplit((p.scheme.lower().replace('http', 'https', 1) if p.scheme == 'http' else p.scheme,
                       p.netloc.lower(), p.path.rstrip('/'), p.query, ''))

def main():
    rows = []
    section = subsection = group = ''
    for line_no, line in enumerate((ROOT/'sources/README.md').read_text().splitlines(), 1):
        if line.startswith('## '):
            section = re.sub('<[^>]+>', '', line[3:]).strip()
            subsection = group = ''
        elif line.startswith('### '):
            subsection = line[4:].strip()
            group = ''
        elif line.startswith('**') and line.endswith('**'):
            group = line.strip('*')
        m = re.match(r'- \*\*`([^`]+)`\*\*\s*(.*)', line)
        if not m:
            continue
        links = re.findall(r'\[\[([^\]]+)\]\((https?://[^)]+)\)\]', m[2])
        if not links:
            continue
        title = m[2].split('[[')[0].strip().rstrip('.')
        paper = next((u for tag, u in links if tag == 'paper'), '')
        code = next((u for tag, u in links if tag == 'code'), '')
        primary = paper or code or links[0][1]
        code_is_paper = bool(code and re.search(r'(arxiv\.org|doi\.org|aclanthology\.org)', code))
        rows.append(dict(entry_id=f'R{len(rows)+1:04}', line=line_no, section=section,
                         subsection=subsection, group=group, venue_label=m[1], title=title,
                         paper_url=paper, code_labeled_url=code, primary_key=canonical(primary),
                         normalized_title=re.sub(r'[^\w]+', '', title.lower()),
                         code_label_points_to_paper=code_is_paper,
                         verification='catalog_only'))
    with (ROOT/'data/repository_catalog.csv').open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    stats = dict(entries=len(rows), distinct_primary_keys=len({r['primary_key'] for r in rows}),
                 distinct_normalized_titles=len({r['normalized_title'] for r in rows}),
                 entries_by_section=dict(collections.Counter(r['section'] for r in rows)),
                 code_label_points_to_paper=[{'entry_id':r['entry_id'],'title':r['title'],'url':r['code_labeled_url']} for r in rows if r['code_label_points_to_paper']],
                 caveat='URL-key and normalized-title counts are separate mechanical deduplication views; neither is an exact count of unique scholarly works. Paper, code, venue and publication status are not verified by this parser.')
    (ROOT/'data/catalog_stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(stats, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
