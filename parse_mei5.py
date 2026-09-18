import re, json, bisect

p = r'C:\Users\VMF CONTABILIDADE\Downloads\LISTA MEI (1).md'
t = open(p, encoding='utf-8', errors='ignore').read()

pres = [(m.group(), m.start()) for m in re.finditer(r'\b\d{4}-', t)]
sufs = [(m.group(), m.start()) for m in re.finditer(r'(?<!\d)(\d\/\d{2})\b', t)]
assert len(pres) == len(sufs)
pairs = [(a[0] + b[0], a[1], b[1]) for a, b in zip(pres, sufs)]

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
    s = re.sub(r'\s+[SN]\s*$', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def last_cell_flag(l):
    cells = [c.strip() for c in l.split('|')]
    cells = [c for c in cells if c]
    if cells and cells[-1] in ('S', 'N'):
        return cells[-1]
    return ''

recs = []
for k, (code, p1, p2) in enumerate(pairs):
    li, lj = line_at(p1), line_at(p2)
    # span do registro: da linha apos o sufixo anterior ate a linha antes do proximo prefixo
    prev_end = line_at(pairs[k - 1][2]) if k > 0 else 0
    next_start = line_at(pairs[k + 1][1]) if k + 1 < len(pairs) else len(lines) - 1
    # ocupacao: INDEPENDENTE acima (ate 3) depois abaixo (ate 4)
    occ = ''
    for j in list(range(li, max(prev_end, li - 4) - 1, -1)) + \
            list(range(li + 1, min(next_start + 1, li + 5))):
        c = clean_occ(lines[j])
        if 'INDEPENDENTE' in c.upper() and len(c) > 12:
            occ = c
            break
    if not occ:  # fallback: linha com (A)/(Ã)
        for j in list(range(li, max(prev_end, li - 4) - 1, -1)) + \
                list(range(li + 1, min(next_start + 1, li + 5))):
            c = clean_occ(lines[j])
            if ('(A)' in c.upper() or '(Ã)' in c.upper()) and len(c) > 15:
                occ = c + ' INDEPENDENTE'
                break
    # flag: primeira celula S/N isolada dentro do span
    flag = ''
    for j in range(prev_end + 1, next_start):
        f = last_cell_flag(lines[j])
        if f:
            flag = f
            break
    recs.append({'cnae': code, 'ocupacao': occ, 'iss': flag})

print('registros:', len(recs))
for r in recs[:4] + recs[20:22]:
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
print('unicos sem flag:', sum(1 for v in uniq.values() if not v['iss']))
bad = [k for k in uniq if not re.fullmatch(r'\d{4}-\d/\d{2}', k)]
print('fora do padrao:', bad)
json.dump(sorted(uniq.values(), key=lambda x: x['cnae']),
          open('simples-nacional-prototipo/mei_cnaes.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('salvo mei_cnaes.json')
