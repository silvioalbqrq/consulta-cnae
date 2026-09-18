import re
t = open('simples-nacional-prototipo/simples-nacional-prototipo_NOVO/pdf.min.js',
         encoding='utf-8', errors='ignore').read()
i = t.find('Setting up fake worker failed')
print('msg encontrada:', i >= 0)
print('trecho:', t[max(0, i - 600):i + 200].replace('\n', ' ')[:800])
print('=====')
j = t.find('pdf.worker')
print('refs a pdf.worker:', t.count('pdf.worker'))
k = t.find('workerSrc')
print('trecho workerSrc:', t[k:k + 400].replace('\n', ' ') if k >= 0 else 'n/a')
