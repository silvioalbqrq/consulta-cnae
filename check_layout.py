h = open('simples-nacional-prototipo/index.html', encoding='utf-8').read()
checks = {
    'nome Consulta CNAE': 'Consulta CNAE' in h,
    'KPIs clicaveis': all(k in h for k in ['id="kT"', 'id="kO"', 'id="kA"', 'id="kV"']),
    'sidebar': all(k in h for k in ['id="fAnexo"', 'id="fDiv"', 'id="fR"', 'Limpar filtros']),
    'tabela resultados': 'id="tb"' in h,
    'drawer detalhe': 'id="drawer"' in h,
    'drawer veil': 'id="veil"' in h,
    'dados.js ref': 'dados.js' in h,
    'exportar CSV': 'consulta-cnae.csv' in h,
    'mostrar mais': 'btnMore' in h,
    'sem layout print': ('Consulta LC 116' not in h) and ('Supersimples' not in h) and ('Radar Tribut' not in h),
}
for k, v in checks.items():
    print(k, v)
print('bytes html:', len(h.encode('utf-8')))
