import json, os

cls = json.load(open('simples-nacional-prototipo/classificacao_simples_23.json', encoding='utf-8'))
base = json.load(open('simples-nacional-prototipo/cnaes.json', encoding='utf-8'))
mini = {b['id']: {'o': b.get('obs', [])[:2], 'a': b.get('ativ', [])[:6]} for b in base}
with open('simples-nacional-prototipo/dados.js', 'w', encoding='utf-8') as f:
    f.write('window.RADAR_DATA=')
    json.dump(cls, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';window.RADAR_BASE=')
    json.dump(mini, f, ensure_ascii=False, separators=(',', ':'))
    f.write(';')
print('DATA', len(cls), '| BASE', len(mini), '| bytes', os.path.getsize('simples-nacional-prototipo/dados.js'))
print('4541206:', [c for c in cls if c['id'] == '4541206'])
