import json, csv

p = 'simples-nacional-prototipo/classificacao_simples_23.json'
cls = json.load(open(p, encoding='utf-8'))
ids = set(x['id'] for x in cls)
if '9900800' not in ids:
    cls.append({'cnae': '9900-8/00', 'id': '9900800',
                'descricao': 'Organismos internacionais e outras instituicoes extraterritoriais',
                'divisao': '99', 'status': 'VEDADO', 'anexos': '', 'fatorR': 'NAO',
                'motivo': 'Organismos internacionais/extraterritoriais - vedado', 'origem': 'regra'})
aliases = {'1610201': ('1610-2/01', '1610-2/03'), '1610202': ('1610-2/02', '1610-2/04'),
           '4541205': ('4541-2/05', '4541-2/06'), '4713001': ('4713-0/01', '4713-0/04'),
           '4713003': ('4713-0/03', '4713-0/05'), '5611202': ('5611-2/02', '5611-2/04')}
have = set(x['id'] for x in cls)
for nid, (cod, novo) in aliases.items():
    if nid not in have:
        cls.append({'cnae': cod, 'id': nid, 'descricao': '[DESATIVADA 2.2] ver ' + novo,
                    'divisao': cod[:2], 'status': 'DESATIVADA', 'anexos': '', 'fatorR': 'NAO',
                    'motivo': 'Codigo 2.2 desativado - usar ' + novo, 'origem': 'alias-2.2'})
json.dump(cls, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open('simples-nacional-prototipo/classificacao_simples_23.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['cnae', 'id', 'descricao', 'divisao', 'status', 'anexos', 'fatorR', 'motivo', 'origem'])
    w.writeheader()
    w.writerows(cls)
from collections import Counter
print(len(cls), dict(Counter(x['status'] for x in cls)))
