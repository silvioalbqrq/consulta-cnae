import re, json

cls = {x['id']: x for x in json.load(
    open('simples-nacional-prototipo/simples-nacional-prototipo_NOVO/classificacao_simples_23.json', encoding='utf-8'))}

def extract(text):
    found = []
    for m in re.finditer(r'\b(\d{2})\s*[.\-–—]?\s*(\d{2})\s*[.\-–—]?\s*(\d)\s*[.\-–—]?\s*(\d{2})\b', text):
        found.append((m.group(1) + m.group(2) + m.group(3) + m.group(4), m.start()))
    for m in re.finditer(r'(?<!\d)(\d{7})(?!\d)', text):
        if m.group(1) in cls:
            found.append((m.group(1), m.start()))
    seen, out = set(), []
    for raw, pos in found:
        if raw not in seen:
            seen.add(raw)
            out.append((raw, pos))
    return sorted(out, key=lambda t: t[1])

def papel(text, pos):
    iS = -1
    m = re.search(r'SECUND[AÁ]RIAS?', text, re.I)
    if m:
        iS = m.start()
    m = re.search(r'ATIVIDADE\s*ECON[OÔ]MICA\s*PRINCIPAL', text, re.I)
    iP = m.start() if m else -1
    if iS >= 0 and pos > iS:
        return 'Secundaria'
    if iP >= 0 and pos > iP:
        return 'Principal'
    return 'Identificada'

# textos dos PDFs vindos da conversa (trechos com CNAEs) + CNPJ.txt
t1 = """43.30-4-04 - Serviços de pintura de edifícios em geral
CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS
Não informada
213-5 - Empresário (Individual) 66.576.500/0001-84"""
t2 = """45.774.997/0001-75 MATRIZ 24/03/2022 NOME EMPRESARIAL MARCELL DIAS MACIEL
CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL (*)
45.30-7-05 - Comércio a varejo de pneumáticos e câmaras-de-ar (Dispensada *)
CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS (*)
45.30-7-03 - Comércio a varejo de peças e acessórios novos para veículos automotores (Dispensada *)
45.41-2-06 - Comércio a varejo de peças e acessórios novos para motocicletas e motonetas (Dispensada *)
213-5 - Empresário (Individual) 60.035-130 (85) 8416-3096"""
t3 = """49.361.849/0001-80 27/01/2023 TSST MARAPONGA LTDA
CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL
64.63-8-00 - Outras sociedades de participação, exceto holdings
CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS
62.01-5-01 - Desenvolvimento de programas de computador sob encomenda
62.02-3-00 - Desenvolvimento e licenciamento de programas de computador customizáveis
62.03-1-00 - Desenvolvimento e licenciamento de programas de computador não-customizáveis
62.09-1-00 - Suporte técnico, manutenção e outros serviços em tecnologia da informação
68.10-2-02 - Aluguel de imóveis próprios
80.20-0-01 - Atividades de monitoramento de sistemas de segurança eletrônico
81.11-7-00 - Serviços combinados para apoio a edifícios, exceto condomínios prediais
82.11-3-00 - Serviços combinados de escritório e apoio administrativo
206-2 - Sociedade Empresária Limitada 60.192-022 (85) 9989-3643"""
t4 = open(r'C:\Users\VMF CONTABILIDADE\Documents\CNPJ.txt', encoding='utf-8', errors='ignore').read()

for i, t in enumerate([t1, t2, t3, t4], 1):
    print(f'--- amostra {i} ---')
    codes = extract(t)
    for raw, pos in codes:
        x = cls.get(raw)
        tag = (x['status'] + ' ' + (x['anexos'] or '')) if x else 'DESCONHECIDO'
        print(f'  {raw} [{papel(t, pos)}] -> {tag}')
    ved = [r for r, _ in codes if cls.get(r, {}).get('status') == 'VEDADO']
    amb = [r for r, _ in codes if cls.get(r, {}).get('status') == 'AMBIGUO']
    print('  VEREDITO:', 'IMPEDIDA ' + str(ved) if ved else ('RESSALVA ' + str(amb) if amb else 'OPTANTE'))
