import re, sys
import esprima
for path in sys.argv[1:]:
    h = open(path, encoding='utf-8').read()
    scripts = re.findall(r'<script>(.*?)</script>', h, re.S)
    js = scripts[-1]
    try:
        esprima.parseScript(js)
        print(path.split('prototipo')[-1], '-> JS VALIDO')
    except Exception as e:
        print(path.split('prototipo')[-1], '-> ERRO:', e)
