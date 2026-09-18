import re, json

mei = json.load(open('simples-nacional-prototipo/mei_cnaes.json', encoding='utf-8'))
recs = []
# reconstroi pares p/ spans
p = r'C:\Users\VMF CONTABILIDADE\Downloads\LISTA MEI (1).md'
t = open(p, encoding='utf-8', errors='ignore').read()
pres = [(m.group(), m.start()) for m in re.finditer(r'\b\d{4}-', t)]
sufs = [(m.group(), m.start()) for m in re.finditer(r'(?<!\d)(\d\/\d{2})\b', t)]
pairs = [(a[0] + b[0], a[1], b[1]) for a, b in zip(pres, sufs)]
lines = t.splitlines()
import bisect
offs, acc = [], 0
for l in lines:
    offs.append(acc)
    acc += len(l) + 1

def line_at(pos):
    return bisect.bisect_right(offs, pos) - 1

by_cnae = {}
for k, (code, p1, p2) in enumerate(pairs):
    li = line_at(p1)
    prev_end = line_at(pairs[k - 1][2]) if k > 0 else 0
    next_start = line_at(pairs[k + 1][1]) if k + 1 < len(pairs) else len(lines) - 1
    by_cnae.setdefault(code, []).append((prev_end, next_start))

fixed = 0
for u in mei:
    if u['iss']:
        continue
    for prev_end, next_start in by_cnae.get(u['cnae'], []):
        for j in range(prev_end + 1, next_start):
            m = re.search(r'\s([SN])\s*\|?\s*$', lines[j].rstrip())
            if m:
                u['iss'] = m.group(1)
                fixed += 1
                break
        if u['iss']:
            break
print('flags recuperadas p/ CNAEs:', fixed)
from collections import Counter
print('flags agora:', Counter(u['iss'] or '?' for u in mei))
print('ainda sem:', [u['cnae'] for u in mei if not u['iss']][:20])
json.dump(mei, open('simples-nacional-prototipo/mei_cnaes.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('salvo')
