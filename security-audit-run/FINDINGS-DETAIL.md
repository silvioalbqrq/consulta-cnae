# Detalhe dos Achados Confirmados — Consulta CNAE

**Metodologia:** cloudflare/security-audit-skill  
**Run ID:** run-1 | **Commit:** `main@5968607`  
**Gerado em:** 2026-11-02  

---

## F-001 — DOM renderização inconsistente: descricao e base injetadas sem escape HTML

**Severidade:** low  
**Veredito:** confirmed

### Descrição
A função `analyzeText` em `index.html` monta o HTML da tabela de análise e injeta os campos `descricao` e `base` da base de dados diretamente via `innerHTML`, sem aplicar a função `esc()` de escape HTML.

### Evidência no source
- `index.html`, linha 519: `+(r.x?r.x.descricao:"<i>não encontrado</i>")+"</td>"`
- `index.html`, linha 520: `"<td><small>"+(r.x&&r.x.base?r.x.base:"—")+"</small></td>"`

Campos da mesma função já usam `esc()` corretamente: `info.razao` (L.512), `info.cnpj` (L.512), `e.name`/`f.name` (L.540). A inconsistência entre campos do mesmo bloco é o defeito.

### Trust boundary
- **Principal de menor confiança:** quem tem gravação na base de dados `dados.js` (desenvolvedor do repo; ou qualquer pessoa com commit no repositório).
- **Input aceito:** campos `descricao` e `base` de `classificacao_simples_23.json` / `cnaes.json`.
- **Controle pretendido:** escape HTML antes de injetar no DOM.
- **Boundary cruzada:** conteúdo da base é renderizado como HTML no navegador do usuário.
- **Principal/recurso afetado:** qualquer usuário que visualize a análise de um CNAE cuja `descricao` ou `base` contenha caracteres HTML.

### Resultado concreto observável
Se `descricao` ou `base` contiverem tags `<`, `>` ou `&`, o layout da tabela `minitab` é quebrado. Existe vetor de auto-XSS / quebra de renderização se um ator com gravação no repo injetar conteúdo HTML malicioso na base.

### Reprodução
1. Editar `classificacao_simples_23.json` inserindo um `descricao` como `<img src=x onerror=alert(1)>`.
2. Regenerar `dados.js` (`python build_dados.py`).
3. Recarregar a análise de qualquer CNAE da base e observar a execução/quebra.

### Menor correção efetiva
Aplicar `esc()` em `r.x.descricao` e `r.x.base` na linha 519-520 de `index.html`, consistente com os demais campos de `analyzeText`.

### Teste de regressão sugerido
Adicionar teste de render confirmando que `descricao` contendo `<script>` é escapado no HTML de saída (não executado).

---

## F-002 — Subresource de terceiros sem integridade (SRI ausente) — tesseract.js via CDN

**Severidade:** medium  
**Veredito:** confirmed

### Descrição
O site carrega o mecanismo de OCR `tesseract.js` de um CDN de terceiros (`jsdelivr`) sem o atributo `integrity` (Subresource Integrity). Se o CDN for comprometido, um script malicioso é executado no contexto de origem de todos os visitantes.

### Evidência no source
- `index.html`, linha 471: `await loadScriptOnce("https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js");`

Não há parâmetro `integrity`. Outros assets (`pdf.min.js`, `pdf.worker.min.js`) são vendados localmente, mostrando que o padrão de vendorizar existe no projeto, mas não foi aplicado ao tesseract.js (provavelmente por tamanho).

### Trust boundary
- **Principal de menor confiança:** operador do CDN `jsdelivr` (terceiro, fora do repositório).
- **Input aceito:** resposta HTTP do script `https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js`.
- **Controle pretendido:** atributo `integrity` (SRI) verificando o hash do script antes da execução.
- **Boundary cruzada:** origem `silvioalbqrq.github.io` executa código originado em `cdn.jsdelivr.net`.
- **Principal/recurso afetado:** todos os visitantes do site, se o CDN for comprometido.

### Resultado concreto observável
Execução de JavaScript arbitrário no contexto de origem do site para todos os usuários, se o conteúdo servido pelo jsdelivr for alterado por um atacante (roubo de dados do formulário de upload, leitura do DOM, etc.).

### Reprodução
Inspecionar o elemento `<script>` carregado do jsdelivr no navegador e confirmar a ausência do atributo `integrity`.

### Menor correção efetiva
Adicionar atributo `integrity` com o hash SHA-384/256 do `tesseract.js@5`, **ou** vendorizar o arquivo localmente (baixar e commitar `tesseract.min.js` no repo, como já feito com `pdf.min.js`).

### Teste de regressão sugerido
Verificar que o `<script>` do tesseract carrega com o atributo `integrity` preenchido; falhar o build se estiver ausente.

---

## F-003 — CSV injection potencial via células descricao / base_legal / motivo

**Severidade:** low  
**Veredito:** confirmed

### Descrição
A exportação CSV (`btnCsv`) insere os campos `descricao`, `base_legal` e `motivo` nas células sem escapar caracteres de fórmula (`=`, `+`, `-`, `@`). Se a base contiver valores iniciando com esses caracteres, um usuário que abra o CSV no Excel poderá ter fórmulas interpretadas (CSV injection).

### Evidência no source
- `index.html`, linhas 387-389: os campos são inseridos no CSV com aspas simples escapando aspas duplas internas, mas **sem** prefixo de escape de fórmula (ex. `'` ou aspas triplas).

### Trust boundary
- **Principal de menor confiança:** autor da base de dados (conteúdo das células exportadas).
- **Input aceito:** campos `descricao`, `base_legal`, `motivo` exportados no CSV.
- **Controle pretendido:** escapar/prefixar células que iniciem com caracteres de fórmula.
- **Boundary cruzada:** o usuário abre o CSV exportado (`consulta-cnae.csv`) em Excel / planilha compatível.
- **Principal/recurso afetado:** usuário que abre o arquivo gerado pelo site.

### Resultado concreto observável
Células iniciando com caracteres de fórmula podem ser interpretadas como fórmulas pelo Excel. A base é controlada pelo desenvolvedor, o que reduz a probabilidade, mas não elimina o vetor.

### Reprodução
Inserir na base um `descricao` iniciando com `=CMD|` (ou `=`, `+`, `-`, `@`) e exportar o CSV; abrir no Excel e observar interpretação como fórmula.

### Menor correção efetiva
Prefixar com apóstrofo (`'`) ou sanitizar células que iniciem com `=`, `+`, `-`, `@` antes de gravar no CSV (`index.html` L.389).

### Teste de regressão sugerido
Teste de export confirmando que células iniciando com `=` são prefixadas e não interpretadas como fórmula.

---

## Observação sobre classificações de severidade

Apenas registros `confirmed` recebem severidade. A alta/média discriminadora é: o resultado demonstrado derrota totalmente um controle explícito para uma ação com consequências reais, ou apenas o enfraquece? Nenhum achado confirmado neste run atinge o limiar de `high` (nenhum controle explícito foi derrotado com consequências reais no contexto do site estático sem servidor).
