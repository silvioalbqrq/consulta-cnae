# Consulta CNAE — Enquadramento no Simples Nacional

Dashboard moderno: barra de busca global, KPIs clicáveis (total/optantes/ambíguos/vedados/MEI), filtros laterais (situação/anexo/divisão/Fator R/MEI), tabela de resultados com ficha em painel lateral, exportação CSV e simulador de alíquota.

## MEI (Anexo XI, Res. CGSN 140/2018, Tabelas A e B)
- 471 ocupações → **351 CNAEs** (`mei_cnaes.json`), todos presentes na base 2.3
- 343 OPTANTE + 8 AMBÍGUO (Anexo V, Fator R não se aplica ao DAS fixo do MEI); 3 exceções aplicadas sobre a regra geral (1220-4/99 fumo, 4929-9/02 fretamento metropolitano, 9700-5/00 diarista)
- Selo MEI na tabela e na ficha (ocupações + ISS no DAS) + filtro "Somente MEI" + CSV com colunas mei/mei_iss/mei_ocupacoes

## Arquivos
- `index.html` — painel VMF (consulta unificada + análise + simulador)
- `classificacao_simples_23.json/csv` — 1.331 subclasses do anexo 2.3 classificadas: OPTANTE / AMBIGUO / VEDADO + anexos + Fator R + motivo
- `anexo_subclasses23.json` — extração do arquivo `CNAE_Subclasses_2_3_Estrutura_Detalhada.md`
- `cnaes.json` — descrições/notas IBGE (API oficial, 1.332)
- `build_classificacao.py` — motor de classificação (curadoria + regras por divisão)

## Resultado da análise (recomeço pelo arquivo correto)
- Planilha Excel 2.401 linhas = ~21 seções + ~87 divisões + ~285 grupos + ~673 classes + 1.331 subclasses + cabeçalhos + ~40 linhas de RESUMO ALTERAÇÕES/preferenciais. Não são 2.401 CNAEs.
- TOTAL 1338 na classificação = 1.331 subclasses 2.3 + 9900-8/00 (IBGE, sem linha na planilha) + 6 aliases 2.2 desativados
- OPTANTE 1116 · AMBIGUO 99 · VEDADO 117 · DESATIVADA 6 (1610-2/01, 1610-2/02, 4541-2/05, 4713-0/01, 4713-0/03, 5611-2/02 → ver correspondentes 2.3)
- Vedados concentrados: div 64 (36), 66 (18), 94 (9), 35 (8), 65 (8), 84 (8), 49 (6)
- Ambíguos concentrados: div 86 saúde (37), 74 (14), 46 representantes (12), 71 (8), 73 (8), 62 TI (5)

Critérios: art. 17 (vedado), Fator R / multi-anexo (ambíguo), resto optante com anexo I–V (LC 123/147/155, CGSN 140/2018).

## Uso
`python3 -m http.server 8000 --directory simples-nacional-prototipo` → `http://localhost:8000/`
