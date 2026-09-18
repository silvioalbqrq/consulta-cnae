import re, sys
path = sys.argv[1]
h = open(path, encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', h, re.S)
js = scripts[-1]
tmp = re.sub(r'"(?:[^"\\]|\\.)*"', '""', js)
tmp = re.sub(r"'(?:[^'\\]|\\.)*'", "''", tmp)
tmp = re.sub(r'`(?:[^`\\]|\\.)*`', '``', tmp, flags=re.S)
tmp = re.sub(r'//[^\n]*', '', tmp)
for a, b in [('{', '}'), ('(', ')'), ('[', ']')]:
    ok = tmp.count(a) == tmp.count(b)
    print(path.split('prototipo')[-1], a + b, tmp.count(a), 'vs',
          tmp.count(b), '->', 'OK' if ok else 'ERRO')
