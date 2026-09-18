import json, csv, os

BASE = 'simples-nacional-prototipo/'
cls = json.load(open(BASE + 'classificacao_simples_23.json', encoding='utf-8'))
mei = json.load(open(BASE + 'mei_cnaes.json', encoding='utf-8'))

def did(s):
    return s.replace('-', '').replace('/', '')

mei_by_id = {did(m['cnae']): m for m in mei}

# Excecoes: Anexo XI autoriza expressamente (prevalece p/ MEI; regra geral mantida na obs)
OVERRIDES = {
    '1220499': {'status': 'OPTANTE', 'anexos': 'II', 'fatorR': 'NAO',
                'motivo': 'Anexo XI autoriza ao MEI (exceto cigarros/cigarrilhas/charutos); no Simples geral validar art.17',
                'origem': 'excecao-MEI'},
    '4929902': {'status': 'OPTANTE', 'anexos': 'III', 'fatorR': 'NAO',
                'motivo': 'Anexo XI autoriza ao MEI (fretamento em regiao metropolitana); intermunicipal geral e vedado',
                'origem': 'excecao-MEI'},
    '9700500': {'status': 'OPTANTE', 'anexos': 'III', 'fatorR': 'NAO',
                'motivo': 'Diarista autonoma permite MEI; vinculo de emprego domestico nao permite Simples',
                'origem': 'excecao-MEI'},
}

n_mei = 0
for x in cls:
    m = mei_by_id.get(x['id'])
    if m:
        x['mei'] = 'SIM'
        x['mei_iss'] = m.get('iss', '')
        x['mei_ocup'] = m.get('ocupacoes', [])[:4]
        n_mei += 1
        if x['id'] in OVERRIDES:
            x.update(OVERRIDES[x['id']])
    else:
        x['mei'] = ''
        x['mei_iss'] = ''
        x['mei_ocup'] = []

json.dump(cls, open(BASE + 'classificacao_simples_23.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
with open(BASE + 'classificacao_simples_23.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['cnae', 'id', 'descricao', 'divisao', 'status', 'anexos',
                                      'fatorR', 'mei', 'mei_iss', 'motivo', 'origem'])
    w.writeheader()
    for x in cls:
        r = dict(x)
        r['mei_ocup'] = ' | '.join(x.get('mei_ocup', []))
        w.writerow({k: r.get(k, '') for k in
                    ['cnae', 'id', 'descricao', 'divisao', 'status', 'anexos',
                     'fatorR', 'mei', 'mei_iss', 'motivo', 'origem']})

# rebuild dados.js
base = json.load(open(BASE + 'cnaes.json', encoding='utf-8'))
mini = {b['id']: {'o': b.get('obs', [])[:2], 'a': b.get('ativ', [])[:6]} for b in base}
with open(BASE + 'dados.js', 'w', encoding='utf-8') as f:
    f.write('window.RADAR_DATA=')
    json.dump(cls, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';window.RADAR_BASE=')
    json.dump(mini, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';')

from collections import Counter
print('total:', len(cls), '| com MEI:', n_mei)
print('status:', dict(Counter(x['status'] for x in cls)))
print('MEI por status:', Counter(x['status'] for x in cls if x.get('mei') == 'SIM'))
print('MEI por anexo:', Counter(x['anexos'] for x in cls if x.get('mei') == 'SIM'))
print('dados.js bytes:', os.path.getsize(BASE + 'dados.js'))
