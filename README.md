# Consulta CNAE — Enquadramento no Simples Nacional

Dashboard estático (GitHub Pages) para consultar as subclasses CNAE 2.3 e ver se a atividade permite o Simples Nacional, qual anexo se aplica, se há Fator R e se permite MEI. Tem busca e filtros, exportação CSV, análise local de cartão CNPJ (PDF/imagem/TXT) e simulador de alíquota efetiva. Tudo roda no navegador.

## Números da base

- 1.338 linhas = 1.331 subclasses 2.3 + 9900-8/00 + 6 aliases 2.2 desativados
- OPTANTE 1.123 · AMBÍGUO 95 · VEDADO 114 · DESATIVADA 6
- 32 linhas marcadas `revisar` (motivo manda "validar/verificar") aparecem com o selo **VALIDAR** na tabela, na ficha e no veredito do arquivo

## MEI (Anexo XI, Res. CGSN 140/2018, Tabelas A e B)

- 471 ocupações → **351 CNAEs** (`mei_cnaes.json`), todos presentes na base 2.3
- 345 OPTANTE + 6 AMBÍGUO; 3 exceções aplicadas sobre a regra geral (1220-4/99 fumo, 4929-9/02 fretamento metropolitano, 9700-5/00 diarista)
- Selo MEI na tabela e na ficha (ocupações + ISS no DAS) + filtro "Somente MEI" + CSV com colunas mei/mei_iss/mei_ocupacoes

## Arquivos

- `index.html` — painel (consulta + análise de arquivo + simulador)
- `logic.js` — lógica pura compartilhada com os testes (extração de CNAE, faixas, veredito)
- `classificacao_simples_23.json/csv` — subclasses classificadas: status + anexos + Fator R + motivo + MEI
- `anexo_subclasses23.json` — extração de `CNAE_Subclasses_2_3_Estrutura_Detalhada.md`
- `cnaes.json` — descrições/notas IBGE (API oficial)
- `mei_cnaes.json` — ocupações MEI (Anexo XI)
- `build_classificacao.py` — motor de classificação (curadoria + regras por divisão)
- `fix_classificacao.py` — adiciona 9900-8/00 e os 6 aliases 2.2
- `mei_update.py` — cruza o Anexo XI, grava `revisar` e reconstrói `dados.js`
- `build_dados.py` — gera `dados.js`
- `build.py` — roda a pipeline completa na ordem correta
- `sw.js` — service worker (network-first para HTML/dados, cache para o resto)

## Build

```bash
python build.py
```

Equivale a `build_classificacao.py` → `fix_classificacao.py` → `mei_update.py` → `build_dados.py`. Rodar só as duas pontas perde MEI, aliases e o campo `revisar`.

## Testes

```bash
node --test test_logic.mjs
```

Cobrem extração de CNAE (`0000-0/00`, `00.00-0-00`, 7 dígitos, sem falsos positivos em CNPJ/telefone), teto de R$ 4,8 mi, piso zero e os vereditos (desconhecido, MEI único, múltiplas atividades MEI, vedado e vedado a validar).

## Uso local

```bash
python3 -m http.server 8000
```

Abra `http://localhost:8000/`. TXT funciona via `file://`; PDF/imagem precisam de HTTP.

## Critérios

Art. 17 (vedado), Fator R / multi-anexo (ambíguo), resto optante com anexo I–V (LC 123/147/155, CGSN 140/2018). Ferramenta educacional — não substitui parecer técnico ou assessoria contábil.
