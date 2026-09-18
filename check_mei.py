import json

mei = json.load(open('simples-nacional-prototipo/mei_cnaes.json', encoding='utf-8'))
cls = json.load(open('simples-nacional-prototipo/classificacao_simples_23.json', encoding='utf-8'))
by_id = {x['id']: x for x in cls}

def did(s):
    return s.replace('-', '').replace('/', '')

print('MEI unicos:', len(mei))
# confere pontuais
for c in ['9602-5/01', '4930-2/02', '7319-0/02', '4724-5/00', '4923-0/02', '5611-2/01']:
    m = next((x for x in mei if x['cnae'] == c), None)
    print(c, '-> iss:', m['iss'] if m else 'AUSENTE', '| ocups:', len(m['ocupacoes']) if m else 0)

falt = [m['cnae'] for m in mei if did(m['cnae']) not in by_id]
print('MEI fora da base 2.3:', falt or 'NENHUM')

from collections import Counter
print('status dos MEI na classificacao:', Counter(by_id[did(m['cnae'])]['status'] for m in mei if did(m['cnae']) in by_id))
print('anexos dos MEI:', Counter(by_id[did(m['cnae'])]['anexos'] or '-' for m in mei if did(m['cnae']) in by_id))
print('MEI com Fator R:', sum(1 for m in mei if did(m['cnae']) in by_id and by_id[did(m['cnae'])]['fatorR'] == 'SIM'))
