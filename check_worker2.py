import json
t = open('simples-nacional-prototipo/simples-nacional-prototipo_NOVO/pdf.worker.min.js',
         encoding='utf-8', errors='ignore').read()
print('bytes:', len(t))
for k in ['getDocument', 'MessageHandler', 'LoopbackPort', 'setup']:
    print(k + ':', k in t)
