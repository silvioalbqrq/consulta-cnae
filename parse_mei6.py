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
    s = re.sub(r'\s+', ' ', s).strip()
    # nome oficial termina em INDEPENDENTE: corta descricao grudada
    m = re.search(r'INDEPENDENTE', s.upper())
    if m:
        s = s[:m.start() + len('INDEPENDENTE')]
    return s.strip()

def last_cell_flag(l):
    cells = [c.strip() for c in l.split('|')]
    cells = [c for c in cells if c]
    if cells and cells[-1] in ('S', 'N'):
        return cells[-1]
    return ''

recs = []
for k, (code, p1, p2) in enumerate(pairs):
    li, lj = line_at(p1), line_at(p2)
    prev_end = line_at(pairs[k - 1][2]) if k > 0 else 0
    next_start = line_at(pairs[k + 1][1]) if k + 1 < len(pairs) else len(lines) - 1
    occ = ''
    for j in list(range(li, max(prev_end, li - 4) - 1, -1)) + \
            list(range(li + 1, min(next_start + 1, li + 5))):
        c = clean_occ(lines[j])
        if 'INDEPENDENTE' in c.upper() and len(c) > 12:
            occ = c
            break
    if not occ:
        for j in list(range(li, max(prev_end, li - 4) - 1, -1)) + \
                list(range(li + 1, min(next_start + 1, li + 5))):
            c = clean_occ(lines[j])
            if ('(A)' in c.upper() or '(Ã)' in c.upper()) and len(c) > 15:
                occ = (c + ' INDEPENDENTE').strip()
                break
    flag = ''
    # 1) dentro do span do registro
    for j in range(prev_end + 1, next_start):
        f = last_cell_flag(lines[j])
        if f:
            flag = f
            break
    # 2) fallback: janela larga ao redor de prefixo/sufixo
    if not flag:
        for j in list(range(max(0, li - 1), min(len(lines), li + 3))) + \
                list(range(max(0, lj - 3), min(len(lines), lj + 3))):
            f = last_cell_flag(lines[j])
            if f:
                flag = f
                break
    recs.append({'cnae': code, 'ocupacao': occ, 'iss': flag})

print('registros:', len(recs))
for r in recs[:6]:
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
print('CNAEs unicos:', len(uniq), '| sem flag:', sum(1 for v in uniq.values() if not v['iss']),
      '| sem ocupacao:', sum(1 for v in uniq.values() if not v['ocupacoes']))
print('ex sem flag:', [v['cnae'] for v in uniq.values() if not v['iss']][:12])
json.dump(sorted(uniq.values(), key=lambda x: x['cnae']),
          open('simples-nacional-prototipo/mei_cnaes.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('salvo mei_cnaes.json')
