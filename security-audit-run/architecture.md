# Arquitetura e Trust Boundaries — Consulta CNAE

## Visão geral do alvo
O `consulta-cnae-site` é um site estático de consulta de CNAEs (Classificação Nacional de Atividades Econômicas) hospedado no GitHub Pages (`https://silvioalbqrq.github.io/consulta-cnae/`). É uma aplicação de página única (SPA) em HTML puro com JavaScript embarcado. Todo o processamento ocorre no navegador do cliente; **não há servidor backend** e o site declara explicitamente "nada é enviado".

## Arquivos do alvo
| Caminho | Papel |
|---|---|
| `index.html` | Shell da SPA, CSS, e toda a lógica de UI, busca, análise de arquivo e simulador (~43 KB). Contém `extractCnaes`, `analyzeText`, `handleFile`, `textFromPdf`, `textFromImage`. |
| `logic.js` | Lógica pura extraída do `index.html` (TAB de alíquotas, `extractCnaes`, `splitSections`, `companyInfo`, `rateFor`, `verdictFor`, `CNAELogic`). Compartilhada com `test_logic.mjs`. |
| `dados.js` | Base de dados embarcada: `window.RADAR_DATA` (1.331 subclasses com status/anexo/fatorR/base/motivo) e `window.RADAR_BASE` (observações/atividades IBGE). Gerado por `build_dados.py`. |
| `sw.js` | Service worker de cache offline (Cache First para assets estáticos). |
| `build_dados.py` | Script Python que gera `dados.js` a partir de `classificacao_simples_23.json` + `cnaes.json`. |
| `classificacao_simples_23.json`, `cnaes.json` | Fontes de dados da base (IBGE + curadoria). |
| `pdf.min.js`, `pdf.worker.min.js` | PDF.js vendado localmente para extração de texto de PDF. |
| `test_logic.mjs` | Testes de unidade (Node) das funções puras de `logic.js`. |

## Trust boundaries
O site é executado inteiramente no contexto de origem única (`silvioalbqrq.github.io`) dentro do navegador do usuário.

- **Boundary 1 — Cliente ↔ Conteúdo do arquivo enviado:** O usuário solta/selecionar um PDF, imagem ou TXT. O conteúdo é lido localmente (`FileReader` / `arrayBuffer`), passado para `extractCnaes` e comparado com a base local `dados.js`. Nenhum dado sai do navegador. Não há cruzamento de origem aqui, mas o conteúdo do arquivo é **não confiável** (pode conter texto arbitrário, tags HTML, sequências longas de dígitos, etc.) e é renderizado no DOM.
- **Boundary 2 — Cliente ↔ CDN de terceiros:** `tesseract.js` é carregado de `https://cdn.jsdelivr.net/...` (OCR de imagem). Isso cruza a trust boundary para um host de terceiros sem controle de integridade (ver F-002).
- **Boundary 3 — Service worker:** `sw.js` intercepta requisições `fetch` da mesma origem e popula o Cache API. Afeta apenas assets da própria origem.

## Input surfaces (não confiáveis)
1. Conteúdo do arquivo enviado (PDF/TXT/imagem via OCR): texto arbitrário que alimenta `extractCnaes`, `splitSections`, `companyInfo` e é injetado via `innerHTML` em `analyzeText`.
2. Query string (`location.search`): parâmetros `q`, `st`, `anexo`, `div`, `fr`, `mei` usados para restaurar filtros/estado. Não chegam a sinks sensíveis de execução.
3. Nome do arquivo (`f.name`): exibido com `esc()` na maior parte dos pontos (ver F-001 para consistência).
4. `window.RADAR_DATA` / `window.RADAR_BASE` de `dados.js`: fonte controlada pelo desenvolvedor, versionada no repo.

## Sinks (renderização / execução)
- `innerHTML` da `#aout` (resultado da análise, tabela `minitab`, veredito, botões "Simular").
- `innerHTML` do `drawer` (ficha do CNAE).
- Tabela de resultados principal (`tb`).
- `location.search` / `history.replaceState` (compartilhamento de filtros via URL).
- `document.title` não modificado dinamicamente com input do usuário.

## Controles de segurança existentes
- Função `esc()` (escape HTML) aplicada a `info.razao`, `info.cnpj`, nome do arquivo em vários pontos.
- `extractCnaes` valida CNAEs contra a base local (`byId7` / `has`) — códigos não encontrados não geram saída de anexo.
- Limite de 15 MB no tamanho do arquivo enviado.
- Leitura de PDF limitada a 10 páginas; OCR com indicador de progresso.
- Service worker somente leitura de assets da mesma origem.
- Não há autenticação, cookies de sessão, JWT, API keys, banco de dados, ou state-changing no servidor.

## Out-of-scope desta auditoria
- Configuração de cabeçalhos HTTP de resposta (GitHub Pages não expõe cabeçalhos customizáveis via repo estático sem workers/headers).
- Comportamento do provedor CDN (jsdelivr) — fora do repositório; registrado como `needs_validation` quando relevante.
- Vulnerabilidades conhecidas na versão específica do PDF.js vendada — requer consulta a banco de vulnerabilidades externo (`needs_validation`).
