# Contribuindo para o projeto

Obrigado por contribuir! 🙏  
Este documento descreve como colaborar de forma segura, eficiente e reprodutível no projeto — incluindo padrões de commits, pull requests e requisitos mínimos de qualidade.

> Aviso importante sobre dados sensíveis  
> Nunca envie dados reais de denúncias ao repositório público. Use dados sintéticos ou amostras anonimizadas. Para problemas sensíveis ou vazamentos, contate o time responsável imediatamente.

---

## Sumário
- [Código de Conduta](#código-de-conduta)
- [Como perguntar / tirar dúvidas](#como-perguntar--tirar-dúvidas)
- [Fluxo de trabalho Git (branching)](#fluxo-de-trabalho-git-branching)
- [Mensagens de Commit](#mensagens-de-commit)
- [Template de Pull Request](#template-de-pull-request)
- [Contato / Team roles](#contato--team-roles)

---

## Código de Conduta
Este projeto segue o [Pacto de Código de Conduta para Colaboradores v2.1](https://www.contributor-covenant.org/pt/version/2/1/code_of_conduct/). Ao contribuir, você concorda em manter um ambiente respeitoso e colaborativo.

---

## Como perguntar / tirar dúvidas
1. Pesquise nas Issues antes de abrir.
2. Se não achar resposta, abra uma *issue* com título claro: `pergunta: <assunto>`.
3. Forneça contexto (passos, versão, logs, ambiente) para chegar no resultado.
4. Para dúvidas sensíveis sobre dados, contate o líder diretamente pelo [e-mail](mailto:marcuspaivamartins@gmail.com).

---

## Fluxo de trabalho Git (branching)
- `main` — código em produção / pronto para deploy. Protegido.
- `develop` — integração e staging.
- `feat/<desc-curta>` — novas funcionalidades.
- `fix/<desc-curta>` — correções de bugs.
- `chore/<desc-curta>` — manutenção, atualização de dependências.
- `data/<desc-curta>` — alterações relacionadas a scripts/metadados de dados.

Nome exemplo: `feat/classificador-spam`

Regras:
- Cada branch corresponde a uma issue. Associe o número da issue no título do PR (ex.: `feat: adicionar filtro de keywords (#123)`).
- Pull Requests precisam de **pelo menos 1 revisor** (ideal 2) e passar o CI (a ser criado) antes do merge.

---

## Mensagens de Commit
Adote o padrão **Conventional Commits** com pequenas extensões úteis para este projeto.

**Formato:**

```plaintext
<tipo>(<escopo>): <assunto>
```
Sendo a seção de **<escopo> opcional**.

**Tipos recomendados:**
- `feat` — nova funcionalidade
- `fix` — correção de bug
- `docs` — documentação
- `style` — formatação, lint, sem mudanças funcionais
- `refactor` — reorganização do código sem alterar comportamento
- `perf` — melhoria de performance
- `test` — adicionar/ajustar testes
- `chore` — tarefas de manutenção  
- `ci` — configuração CI/CD  
- `data` — scripts/metadados de dados (sem incluir dados brutos)  
- `ml` — mudanças no código de ML/experimentos/modelos  
- `mlops` — infra/artefatos de ML (model registry, deploy)

**Exemplos válidos**

- feat(classifier): adicionar pipeline de embeddings
- fix(api): corrigir validação de payload em /analisar
- data(prep): adicionar script de normalização CSV
- ml(treino): salvar métricas de treino em JSON
- docs(contrib): adicionar guia de contribuição

**Regras práticas:**
- Use uma frase curta escrita no presente para o `<assunto>` (<= 72 caracteres).
- Corpo do commit (se necessário) explique *porquê* a mudança e *como* (contexto).
- Referencie issues com `#N` no corpo do commit quando pertinente.

Veja [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/) para referência e exemplos.

---

## Template de Pull Request

```markdown
# Título curto e descritivo
feat(classifier): adicionar filtro de keywords no pré-processamento

## Descrição
Resumo do que foi feito e por quê.

## Tipo de mudança
- [ ] feat
- [ ] fix
- [ ] docs
- [ ] refactor
- [ ] test
- [ ] data
- [ ] ml
- [ ] mx (ops)

## Issue relacionada
Closes #<numero-issue> (se aplicável)

## Como testar
1. Comando para rodar
2. Testes unitários a executar

## Checklist de PR (obrigatório)
- [ ] Testes adicionados/atualizados e passando (`pytest`)
- [ ] Documentação atualizada (README, docs/)
- [ ] Não há dados sensíveis no PR (ver runbook)
- [ ] CI passou (build, lint, testes)

## Impacto em produção
Descrição de possíveis impactos.

## Notas adicionais
Observações para o revisor (ex.: dependências, decisões arquiteturais).
```
