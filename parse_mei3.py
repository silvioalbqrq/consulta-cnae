import re, json

p = r'C:\Users\VMF CONTABILIDADE\Downloads\LISTA MEI (1).md'
t = open(p, encoding='utf-8', errors='ignore').read()

pres = [(m.group(), m.start()) for m in re.finditer(r'\b\d{4}-', t)]
sufs = [(m.group(), m.start()) for m in re.finditer(r'(?<!\d)(\d\/\d{2})\b', t)]
assert len(pres) == len(sufs), (len(pres), len(sufs))
pairs = [(a[0] + b[0], a[1], b[1]) for a, b in zip(pres, sufs)]

lines = t.splitlines()
# offsets de inicio de cada linha
offs, acc = [], 0
for l in lines:
    offs.append(acc)
    acc += len(l) + 1

def line_at(pos):
    import bisect
    return bisect.bisect_right(offs, pos) - 1

def clean(s):
    s = re.sub(r'\|', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

recs = []
for code, p1, p2 in pairs:
    li = line_at(p1)
    occ, flag = '', ''
    # occupation: nearest line at/before prefix with INDEPENDENTE (ate 6 linhas acima) ou longa em caps
    for j in range(li, max(-1, li - 8), -1):
        c = clean(lines[j])
        if 'INDEPENDENTE' in c.upper() and len(c) > 8:
            occ = c
            break
    else:
        for j in range(li, max(-1, li - 8), -1):
            c = clean(lines[j])
            if len(c) > 15 and sum(ch.isalpha() for ch in c) > 10:
                occ = c
                break
    # flag S/N: procura celula isolada nas linhas li-2..li2 do sufixo
    lj = line_at(p2)
    for j in range(max(0, lj - 2), min(len(lines), lj + 3)):
        cells = [c.strip() for c in lines[j].split('|')]
        cells = [c for c in cells if c]
        if cells and cells[-1] in ('S', 'N'):
            flag = cells[-1]
            break
    recs.append({'cnae': code[:4] + '-' + code[4:], 'ocupacao': occ, 'iss': flag})

print('registros:', len(recs))
# amostra
for r in recs[:6] + recs[100:103]:
    print(r)
# quantos sem ocupacao / sem flag
print('sem ocupacao:', sum(1 for r in recs if not r['ocupacao']))
print('sem flag:', sum(1 for r in recs if not r['iss']))
from collections import Counter
print('flags:', Counter(r['iss'] or '?' for r in recs))
json.dump(recs, open('simples-nacional-prototipo/mei_extracao.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
uniq = {}
for r in recs:
    u = uniq.setdefault(r['cnae'], {'cnae': r['cnae'], 'ocupacoes': [], 'iss': ''})
    if r['ocupacao'] and r['ocupacao'] not in u['ocupacoes']:
        u['ocupacoes'].append(r['ocupacao'])
    if r['iss'] and not u['iss']:
        u['iss'] = r['iss']
print('CNAEs unicos:', len(uniq))
json.dump(sorted(uniq.values(), key=lambda x: x['cnae']),
          open('simples-nacional-prototipo/mei_cnaes.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('salvo mei_cnaes.json')
