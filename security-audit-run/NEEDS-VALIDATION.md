# Itens que Precisam de Validação — Consulta CNAE

**Metodologia:** cloudflare/security-audit-skill  
**Run ID:** run-1 | **Commit:** `main@5968607`  
**Gerado em:** 2026-11-02  

---

Registros `needs_validation` têm um fato em aberto específico e **não possuem severidade**. Não são vulnerabilidades confirmadas; são hipóteses baseadas no source que dependem de fatores fora do repositório (deployment, dependências vendadas, configuração de ambiente) para serem confirmadas ou descartadas.

---

## NV-001 — PDF malicioso processado pelo PDF.js vendado localmente

**Fato em aberto:** a versão vendada de `pdf.min.js` / `pdf.worker.min.js` contém vulnerabilidades conhecidas de renderer (execução de código ao abrir um PDF malicioso)?

### Por que está aqui
O site processa PDFs enviados pelo usuário localmente via PDF.js (`index.html`, `textFromPdf`, L.448), usando arquivos vendados (`pdf.min.js`, `pdf.worker.min.js`). Um PDF malicioso poderia explorar uma vulnerabilidade conhecida do renderer do PDF.js para executar código no contexto do navegador do próprio usuário. Não há evidência no source de que isso ocorra; requer consulta externa a banco de vulnerabilidades.

### Safe check (proprietário)
Consultar banco de vulnerabilidades (CVE / GitHub advisories / Mozilla pdf.js advisories) para a **versão exata** dos arquivos vendados `pdf.min.js` e `pdf.worker.min.js`. Se houver CVE de renderer confirmada para aquela versão, atualizar o arquivo vendado para uma versão corrigida.

### Ação do proprietário
- Identificar a versão do `pdf.min.js` vendado.
- Consultar advisories conhecidos para essa versão.
- Se houver CVE relevante, substituir o arquivo vendado pela versão corrigida.
- Considerar isolar o processamento de PDF em um Web Worker para reduzir a superfície de exposição do DOM principal.

---

## NV-002 — Ausência de cabeçalhos de segurança (CSP, X-Frame-Options, etc.) no deployment

**Fato em aberto:** o deployment GitHub Pages aplica cabeçalhos de segurança (Content-Security-Policy, X-Frame-Options, Referrer-Policy, etc.)?

### Por que está aqui
O repositório é um site estático sem mecanismo nativo para definir cabeçalhos de resposta HTTP via HTML. Cabeçalhos de segurança são uma preocupação de deployment/infraestrutura, não de source. Sem inspecionar a resposta ao vivo, não é possível confirmar nem descartar a ausência.

### Safe check (proprietário)
Acessar `https://silvioalbqrq.github.io/consulta-cnae/` e inspecionar os headers de resposta HTTP. Verificar presença de `Content-Security-Policy`, `X-Frame-Options`, `Referrer-Policy`.

### Ação do proprietário
- Se ausentes, configurar cabeçalhos de segurança no provedor de hospedagem (ou avaliar alternativas compatíveis com GitHub Pages).
- Ausência de CSP/X-Frame-Options é um achado de **hardening de deployment**, não de source.

---

## NV-003 — Uso de `(0,eval)(t)` para carregar dados.js

**Fato em aberto:** existe algum caminho onde `dados.js` poderia ser sobrescrito ou injetado por fonte não confiável antes do `eval`?

### Por que está aqui
`index.html` (L.317-318) carrega `dados.js` via `fetch` e executa com `(0,eval)(t)`. `dados.js` define `window.RADAR_DATA` e `window.RADAR_BASE`. Atualmente o arquivo vem do próprio repo (fonte confiável, versionado), mas o padrão de `fetch + eval` cria um vetor se o arquivo alguma vez for servido de origem não confiável ou injetado.

### Safe check (proprietário)
Confirmar que `dados.js` é sempre servido do próprio repositório e não aceita gravação externa. Avaliar a substituição por inclusão estática.

### Ação do proprietário
Substituir o `fetch + (0,eval)` por inclusão estática `<script src="dados.js?v=...">` no HTML, removendo completamente o vetor de execução dinâmica (`eval`).

---

## Nota sobre registros rejeitados

Os registros `rejected` (R-001 a R-004) foram analisados e descartados no source: não há autenticação/CSRF, não há SQL injection (sem banco de dados), não há LLM/prompt injection (sem modelo de linguagem), e não há secrets/chaves de API hardcoded no código-fonte. Detalhes em `findings.json` (seção `rejected`).
