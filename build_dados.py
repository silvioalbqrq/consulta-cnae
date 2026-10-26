import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
def P(name):
    return os.path.join(BASE, name)

cls = json.load(open(P('classificacao_simples_23.json'), encoding='utf-8'))
base = json.load(open(P('cnaes.json'), encoding='utf-8'))
mini = {b['id']: {'o': b.get('obs', [])[:2], 'a': b.get('ativ', [])[:6]} for b in base}
with open(P('dados.js'), 'w', encoding='utf-8') as f:
    f.write('window.RADAR_DATA=')
    json.dump(cls, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';window.RADAR_BASE=')
    json.dump(mini, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';')
print('DATA', len(cls), '| BASE', len(mini), '| bytes', os.path.getsize(P('dados.js')))
print('4541206:', [c for c in cls if c['id'] == '4541206'])
