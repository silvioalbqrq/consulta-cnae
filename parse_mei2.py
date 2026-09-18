import re

p = r'C:\Users\VMF CONTABILIDADE\Downloads\LISTA MEI (1).md'
lines = open(p, encoding='utf-8', errors='ignore').read().splitlines()

# Ocupacoes: linhas com INDEPENDENTE (a maioria) - conta
occ = [l for l in lines if 'INDEPENDENTE' in l.upper()]
print('linhas com INDEPENDENTE:', len(occ))

# Flags S/N isoladas em coluna: linhas cujo ultimo campo e S ou N
flag = []
for l in lines:
    parts = [c.strip() for c in l.split('|')]
    parts = [c for c in parts if c]
    if parts and parts[-1] in ('S', 'N') and len(parts[-1]) == 1:
        flag.append(parts[-1])
from collections import Counter
print('flags S/N encontradas:', len(flag), Counter(flag))

# Tabela B comeca onde?
for i, l in enumerate(lines):
    if 'TABELA B' in l.upper():
        print('TABELA B na linha:', i + 1)
        break
