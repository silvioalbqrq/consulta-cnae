import json
from collections import Counter
cls = json.load(open('simples-nacional-prototipo/classificacao_simples_23.json', encoding='utf-8'))
print('total:', len(cls), '| sem base:', sum(1 for x in cls if not x.get('base')))
print(Counter(x['base'] for x in cls))
for k in ['7319099', '7319001', '7319002', '7319003', '7319004', '7311400',
          '6201501', '4723700', '6911701', '3513100', '9900800', '1610201',
          '1220499', '4929902', '9700500', '6202300', '7111100']:
    x = next(v for v in cls if v['id'] == k)
    print(k, '|', x['status'], '|', x['anexos'], '|', x['fatorR'], '|', x['base'], '|', x['motivo'][:60])
