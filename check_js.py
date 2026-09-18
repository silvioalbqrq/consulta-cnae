import re
h = open('simples-nacional-prototipo/simples-nacional-prototipo_NOVO/index.html',
         encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', h, re.S)
print('blocos script inline:', len(scripts))
js = scripts[-1]
tmp = re.sub(r'"(?:[^"\\]|\\.)*"', '""', js)
tmp = re.sub(r"'(?:[^'\\]|\\.)*'", "''", tmp)
tmp = re.sub(r'`(?:[^`\\]|\\.)*`', '``', tmp, flags=re.S)
tmp = re.sub(r'//[^\n]*', '', tmp)
for a, b in [('{', '}'), ('(', ')'), ('[', ']')]:
    ok = tmp.count(a) == tmp.count(b)
    print(a + b, tmp.count(a), 'vs', tmp.count(b), '->', 'OK' if ok else 'ERRO')
keys = ['loadScriptOnce', 'setProg', 'byId7', 'extractCnaes', 'textFromPdf',
        'textFromImage', 'splitSections', 'companyInfo', 'analyzeText',
        'fmtC', 'handleFile']
print('funcoes analyzer:', all(k in js for k in keys))
