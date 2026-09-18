import re, json, bisect

p = r'C:\Users\VMF CONTABILIDADE\Downloads\LISTA MEI (1).md'
t = open(p, encoding='utf-8', errors='ignore').read()

pres = [(m.group() + '', m.start()) for m in re.finditer(r'\b\d{4}-', t)]
sufs = [(m.group(), m.start()) for m in re.finditer(r'(?<!\d)(\d\/\d{2})\b', t)]
assert len(pres) == len(sufs)
pairs = [(a[0] + b[0], a[1], b[1]) for a, b in zip(pres, sufs)]  # codigo ja completo

lines = t.splitlines()
offs, acc = [], 0
for l in lines:
    offs.append(acc)
    acc += len(l) + 1

def line_at(pos):
    return bisect.bisect_right(offs, pos) - 1

def clean_occ(s):
    s = re.sub(r'\|', ' ', s)
    s = re.sub(r'\b\d{4}-', ' ', s)
    s = re.sub(r'(?<!\d)\d\/\d{2}\b', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+[SN]\s*$', '', s)  # flag solta no fim
    s = re.sub(r'\s+', ' ', s).strip()
    return s

recs = []
for code, p1, p2 in pairs:
    li, lj = line_at(p1), line_at(p2)
    occ = ''
    # janela ao redor do prefixo: prefere linha com INDEPENDENTE mais proxima
    best, bestd = '', 99
    for j in range(max(0, li - 3), min(len(lines), li + 5)):
        c = clean_occ(lines[j])
        if 'INDEPENDENTE' in c.upper() and len(c) > 12:
            d = abs(j - li)
            if d < bestd:
                best, bestd = c, d
    occ = best
    if not occ:
        for j in range(max(0, li - 3), min(len(lines), li + 5)):
            c = clean_occ(lines[j])
            if len(c) > 20:
                occ = c
                break
    flag = ''
    for j in list(range(max(0, li - 1), min(len(lines), li + 3))) + \
            list(range(max(0, lj - 3), min(len(lines), lj + 3))):
        cells = [c.strip() for c in lines[j].split('|')]
        cells = [c for c in cells if c]
        if cells and cells[-1] in ('S', 'N'):
            flag = cells[-1]
            break
    recs.append({'cnae': code, 'ocupacao': occ, 'iss': flag})

print('registros:', len(recs))
for r in recs[:8]:
    print(r)
print('sem ocupacao:', sum(1 for r in recs if not r['ocupacao']))
print('sem flag:', sum(1 for r in recs if not r['iss']))
from collections import Counter
print('flags:', Counter(r['iss'] or '?' for r in recs))

uniq = {}
for r in recs:
    u = uniq.setdefault(r['cnae'], {'cnae': r['cnae'], 'ocupacoes': [], 'iss': ''})
    if r['ocupacao'] and r['ocupacao'] not in u['ocupacoes']:
        u['ocupacoes'].append(r['ocupacao'])
    if r['iss'] and not u['iss']:
        u['iss'] = r['iss']
print('CNAEs unicos:', len(uniq))
# confere formato
bad = [k for k in uniq if not re.fullmatch(r'\d{4}-\d/\d{2}', k)]
print('fora do padrao:', bad)
json.dump(sorted(uniq.values(), key=lambda x: x['cnae']),
          open('simples-nacional-prototipo/mei_cnaes.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('salvo mei_cnaes.json')
