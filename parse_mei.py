import re, json

p = r'C:\Users\VMF CONTABILIDADE\Downloads\LISTA MEI (1).md'
t = open(p, encoding='utf-8', errors='ignore').read()
lines = t.splitlines()
print('linhas:', len(lines))

# Codigos quebrados em duas partes: "4724-" ... "5/00".
# Coleta tokens na ordem e emparelha.
pre = re.findall(r'\b\d{4}-', t)
suf = re.findall(r'(?<!\d)(\d\/\d{2})\b', t)
print('prefixos NNNN-:', len(pre), '| sufixos N/NN:', len(suf))
print('5 primeiros pares:', list(zip(pre, suf))[:5])

full = [a + b for a, b in zip(pre, suf)]
print('reconstruidos:', len(full), '| unicos:', len(set(full)))

# Linha de cada par: tenta capturar ocupacao (texto em maiusculas antes) e flag S/N (apos)
# Estrategia simples por linha: se a linha tem prefixo e sufixo juntos ou proximos
rows = []
for i, l in enumerate(lines):
    m1 = re.findall(r'\b\d{4}-', l)
    m2 = re.findall(r'(?<!\d)(\d\/\d{2})\b', l)
    if m1 or m2:
        rows.append((i + 1, l.strip()[:150]))
print('linhas com fragmentos de codigo:', len(rows))
for r in rows[:8]:
    print(r)
