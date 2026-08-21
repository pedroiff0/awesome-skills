---
name: lattes-xml-projetos
description: Use when gerar, limpar ou inserir itens de bolsa/projetos de pesquisa (PARTICIPACAO-EM-PROJETO / PROJETO-DE-PESQUISA) em XML de importação do Currículo Lattes. Cobre a estrutura de ATUACOES-PROFISSIONAIS, a limpeza de caracteres para ISO-8859-1 e a validação por well-formedness com xmllint (a DTD antiga de 2004 em Downloads não valida o formato novo).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [lattes, xml, curriculo, bolsa, pesquisa, importacao]
    related_skills: [latex-cv-maintenance]
---

# Lattes XML - Itens de Bolsa/Projetos

## Overview
Gera ou reconstrói o trecho de importação XML do Currículo Lattes que contém os itens de
bolsa e projetos de pesquisa (seção `ATUACOES-PROFISSIONAIS` → `ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO`).
Útil para limpar um currículo, inserir só os projetos em que o usuário participou, ou converter
um texto livre (datas, título, descrição, equipe, financiador) em entradas `PROJETO-DE-PESQUISA`.

## When to Use
- O usuário pede para "limpar" ou "inserir" itens de bolsa/projeto no Lattes em formato XML.
- Precisa converter um texto solto (datas + título + descrição + equipe + financiador) em entradas válidas.
- Não usar para produção bibliográfica, orientações ou dados pessoais (são outras seções).
- Para manter o LaTeX CV em sincronia com estes dados (títulos/datas/cargos), ver skill `latex-cv-maintenance`.

## Estrutura do XML (formato NOVO de importação do Lattes)
O formato canônico (idêntico ao exportado pelo próprio site, ex.: `Lattes_final.xml`) é:
```
CURRICULO-VITAE
  DADOS-GERAIS            (atributo NOME-COMPLETO, nao elemento filho)
    RESUMO-CV
    ENDERECO
    FORMACAO-ACADEMICA-TITULACAO?
    IDIOMAS?
  ATUACOES-PROFISSIONAIS
    ATUACAO-PROFISSIONAL
      VINCULOS TIPO-DE-VINCULO="Bolsista" ...
      ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO
        PARTICIPACAO-EM-PROJETO
          PROJETO-DE-PESQUISA (atributos abaixo, auto-fechante)
```
`PROJETO-DE-PESQUISA` é auto-fechante (não tem filhos `EQUIPE`/`FINANCIADOR` em importação
mínima de bolsas — o importador do Lattes preenche equipe/financeiro à parte). A DTD antiga
de 2004 exigia filhos, mas o formato novo NÃO os usa; por isso ela não valida (ver Validação).

## Atributos de PROJETO-DE-PESQUISA
- `NOME-DO-PROJETO` (CDATA)
- `NATUREZA`: `PESQUISA` | `EXTENSAO` | `DESENVOLVIMENTO` | `OUTRA`
- `SITUACAO`: `EM_ANDAMENTO` | `CONCLUIDO` | `DESATIVADO`
- `ANO-INICIO` / `ANO-FIM` (deixe `ANO-FIM=""` se for atual)
- `NUMERO-GRADUACAO`: conta de graduandos como string (ex.: "1", "4", "0")
- `DESCRICAO-DO-PROJETO` (texto livre; manter fiel ao original, só normalizar caracteres)
- Em `PARTICIPACAO-EM-PROJETO`: `FLAG-PERIODO="ATUAL"` para em andamento, `"ANTERIOR"` para concluídos.

## Limpeza de caracteres (encoding ISO-8859-1)
O arquivo deve ser escrito em ISO-8859-1. Substituir antes de gerar:
- `—` (em dash) e `–` (en dash) → `-`
- aspas curvas `“` `”` `‘` `’` → `"` ou `'`
- `→` → `->`; `≈` → `~`; `•` → `-`; nbsp/` ` → espaço
- Escrever com `open(path, "w", encoding="iso-8859-1", errors="replace")`.
- Escapar `&`, `<`, `>`, `"` nos atributos (use `html.escape(s, quote=True)`).

## Validação
- **Well-formedness (obrigatório):** `xmllint --noout arquivo.xml` → deve sair 0, sem mensagem.
- **NÃO valide contra a `LMPLCurriculo.DTD` que fica em Downloads.** Ela é da versão 1.4.1/2.0
  (2004-2006) e NÃO declara `ATUACOES-PROFISSIONAIS` como filha de `CURRICULO-VITAE`, nem
  `NOME-COMPLETO-DO-CURRICULO`. Ela falha até para os XMLs "oficiais" do usuário (ex.: `Lattes_final.xml`).
  O importador do Lattes aceita o formato novo bem-formado; o erro da DTD antiga é esperado e deve ser ignorado.

## Gerador reutilizável
Use `scripts/gerar_projeto_lattes.py`: edite a lista `PROJETOS` (dicionários) e rode
`python3 gerar_projeto_lattes.py`. Ele emite `Lattes_bolsas.xml` em ISO-8859-1, já limpo e
well-formed, no formato canônico (sem EQUIPE/FINANCIADOR — o importador do Lattes preenche
isso depois). Cada projeto:
```python
{
  "nome": "...", "natureza": "PESQUISA", "ano_ini": "2024", "mes_ini": "1",
  "ano_fim": "", "mes_fim": "", "situacao": "EM_ANDAMENTO",
  "desc": "...",
}
```
`mes_ini`/`mes_fim` são opcionais (string vazia se não souber). `ANO-FIM=""` para em andamento.

## Common Pitfalls
1. **Validar contra a DTD antiga** → erro esperado; ignore e confie no well-formedness.
2. **Encoding UTF-8** → o Lattes espera ISO-8859-1; acentos devem vir como bytes ISO-8859-1 (sem `�`).
3. **Usar EQUIPE/FINANCIADOR dentro de PROJETO-DE-PESQUISA** → no formato mínimo de importação
   de bolsas, `PROJETO-DE-PESQUISA` é auto-fechante; equipe e financiador são cadastrados à parte
   no site. Incluir esses elementos quebra a importação mínima.
4. **Texto solto no final** (ex.: "Pedro Henrique Rocha de Andrade. Simulando o impacto de satélites...")
   → tratar como projeto próprio de IC se fizer sentido (foi o caso do item de 2025).
5. **NOME-COMPLETO como elemento filho de DADOS-GERAIS** → no formato novo é ATRIBUTO
   (`<DADOS-GERAIS NOME-COMPLETO="...">`), não elemento.

## Verification Checklist
- [ ] `xmllint --noout <arquivo>` retorna exit 0 (sem mensagem)
- [ ] Todos os projetos do usuário presentes, sem ruído/duplicação
- [ ] `ANO-FIM=""` nos em andamento; `SITUACAO` coerente (EM_ANDAMENTO/CONCLUIDO)
- [ ] `PROJETO-DE-PESQUISA` é auto-fechante (sem EQUIPE/FINANCIADOR dentro)
- [ ] Sem `?`/`�` no arquivo (encoding ISO-8859-1 correto)
