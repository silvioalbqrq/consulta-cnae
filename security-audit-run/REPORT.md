# Relatório de Auditoria de Segurança — Consulta CNAE

**Repositório:** silvioalbqrq/consulta-cnae (consulta-cnae-site)  
**Metodologia:** cloudflare/security-audit-skill (6 fases, full audit mode, perfil `standard`)  
**Commit auditado:** `main@5968607` (working tree limpo, sincronizado com `origin/main`)  
**Gerado em:** 2026-11-02  
**Run ID:** run-1  

---

## Resumo executivo

O site Consulta CNAE é uma aplicação estática de página única que roda inteiramente no navegador (GitHub Pages). Não há servidor backend, autenticação, banco de dados, nem envio de dados para terceiros — todo o processamento de PDF/imagem/TXT ocorre localmente. Isso elimina naturalmente classes inteiras de vulnerabilidades (SQL injection, CSRF, session fixation, exposição de secrets, prompt injection/LLM).

A auditoria confirmou **3 achados** (todos de baixo a médio impacto) e identificou **3 itens que precisam de validação do proprietário** (dependem de fatores de deployment ou dependências vendadas). Nenhum achado de severidade crítica ou alta foi confirmado no código-fonte do repositório.

## Vereditos

| Veredito | Quantidade |
|---|---|
| confirmed | 3 |
| needs_validation | 3 |
| rejected | 4 |

## Achados confirmados (severidade)

| ID | Título | Severidade | Arquivo |
|---|---|---|---|
| F-001 | DOM renderização inconsistente: descricao e base injetadas sem escape HTML | low | `index.html` L.519-520 |
| F-002 | Subresource de terceiros sem integridade (SRI ausente) — tesseract.js via CDN | medium | `index.html` L.471 |
| F-003 | CSV injection potencial via células descricao / base_legal / motivo | low | `index.html` L.387-389 |

## Itens que precisam de validação (não confirmados no source)

| ID | Título | Fato em aberto |
|---|---|---|
| NV-001 | PDF malicioso processado pelo PDF.js vendado localmente | versão vendada tem CVEs de renderer conhecidas? |
| NV-002 | Ausência de cabeçalhos de segurança (CSP, X-Frame-Options) no deployment | o GitHub Pages aplica esses cabeçalhos? |
| NV-003 | Uso de `(0,eval)(t)` para carregar dados.js | dados.js pode ser sobrescrito por fonte não confiável? |

## Recomendações prioritárias (menor esforço efetivo)

1. **F-001:** aplicar `esc()` em `r.x.descricao` e `r.x.base` na tabela de análise (`index.html` L.519-520), consistente com os demais campos da mesma função.
2. **F-002:** adicionar atributo `integrity` (SRI) ao `<script>` do tesseract.js, ou vendorizar o arquivo localmente (como já feito com `pdf.min.js` e `pdf.worker.min.js`).
3. **F-003:** prefixar com apóstrofo (`'`) ou sanitizar células CSV que iniciem com `=`, `+`, `-`, `@` (`index.html` L.389).
4. **NV-001:** verificar a versão de `pdf.min.js`/`pdf.worker.min.js` contra advisories conhecidos (CVE) de renderer do PDF.js.
5. **NV-003:** substituir `fetch + (0,eval)` por inclusão estática `<script src="dados.js">`, removendo o vetor de execução dinâmica.

## Cobertura

A auditoria cobriu todas as superfícies de entrada e classes de ataque aplicáveis ao alvo (DOM rendering, subresource/CDN, execução dinâmica, export CSV, service worker, processamento de PDF, auth/sessão, LLM/agente, secrets, protocolo HTTP/cache, exaustão de recursos, isolamento de dados). Uma única passagem não exaure o alvo; recomenda-se reexecutar após alterações em `dados.js`, `index.html`, dependências vendadas ou mudança de deployment.

Os artefatos detalhados estão em:
- `security-audit-run/architecture.md` — mapeamento de arquitetura, trust boundaries, input surfaces e sinks.
- `security-audit-run/coverage-ledger.json` — unidades de cobertura e mapeamento para findings.
- `security-audit-run/findings.json` — registros estruturados (confirmed / needs_validation / rejected).
- `security-audit-run/FINDINGS-DETAIL.md` — detalhe de cada achado confirmado.
- `security-audit-run/NEEDS-VALIDATION.md` — detalhe de cada item pendente de validação.
