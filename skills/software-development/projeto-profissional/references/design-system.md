# Sistema visual do template (DESIGN.md)

O template carrega um `DESIGN.md` na raiz — spec aberto do Google
(`@google/design.md`): front matter YAML com tokens normativos + prosa
explicando o porquê. Serve para agentes de código consumirem a identidade
visual sem adivinhar.

Ao clonar o template para um projeto novo, o `DESIGN.md` vem junto. Troque
`colors.primary` e a identidade inteira acompanha, incluindo os ícones
(usam `stroke="currentColor"`).

## Regra que não pode ser quebrada: token espelha o CSS

Um DESIGN.md que descreve uma paleta que o código não usa é pior que nenhum.
**Extraia os valores do CSS real**, nunca invente uma paleta bonita.

Depois de escrever, confira token por token contra a folha de estilo. Foi
assim que se descobriu que a prosa afirmava algo falso sobre um cinza —
ver "Contraste" abaixo.

## Ordem canônica das seções (o lint rejeita fora de ordem)

Overview · Colors · Typography · Layout · Elevation & Depth · Shapes ·
Components · Do's and Don'ts

## Lint, exports e o aviso `orphaned-tokens`

```bash
npx -y @google/design.md lint DESIGN.md                                  # meta: 0 erros, 0 avisos
npx -y @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json
npx -y @google/design.md export --format dtcg     DESIGN.md > tokens.json
```

`orphaned-tokens` (token definido e nunca referenciado por componente) dispara
bastante quando a paleta vem de CSS real: `neutral`, `border`, `muted`,
`subtle`, `success` existem no código mas não mapeiam para um botão.

**Não apague o token para silenciar o aviso** — ele existe no CSS por um
motivo. Adicione o componente que de fato o usa:

| Token órfão | Componente que o consome |
|---|---|
| `neutral` | `page` (fundo da página) |
| `border` | `divider` |
| `subtle` | `card-meta` |
| `muted` | `section-lead` |
| `success` / `error` | `alert-success` / `alert-error` |

O aviso está dizendo que a lista de componentes está incompleta, não que o
token sobra.

## Contraste: meça, não estime

Cinzas próximos são visualmente indistinguíveis e decisivos para acessibilidade.
Valores medidos neste template:

| Cor | Sobre | Razão | Veredito |
|---|---|---|---|
| `#94a3b8` | branco | **2.56:1** | reprova AA |
| `#64748b` | branco | 4.76:1 | AA ok |
| `#475569` | branco | 7.5:1 | AAA ok |
| `#94a3b8` | `#0f172a` | 6.96:1 | AA ok (rodapé escuro) |
| `#b6c2d1` | `#0f172a` | 9.88:1 | AAA ok |
| `#2563eb` | branco | 5.17:1 | AA ok |

Armadilha real: a prosa dizia "`#94a3b8` foi removido do texto corrido", mas o
grep mostrava 5 ocorrências. O CSS estava certo (o único uso sobre branco é
sobrescrito depois na cascata) — a **redação** é que era vaga. Ao afirmar algo
sobre o código no DESIGN.md, verifique a afirmação com grep e reescreva com o
número medido em vez de adjetivo.

Fórmula de contraste (WCAG), sem dependência:

```python
def lum(h):
    c = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    c = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0] + .7152*c[1] + .0722*c[2]

def cr(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True)
    return (l1 + .05) / (l2 + .05)      # >= 4.5 para AA em texto pequeno
```

## Não deixe o arquivo virar documentação morta

Depois de criar, amarre-o ao resto do repo, senão ninguém o lê:

- `AGENTS.md`: regra "interface segue o DESIGN.md; mudou visual, atualize o
  token e rode o lint" + proibição de emoji e de cinza novo sem medir.
- `README.md`: link na seção Documentação, com o comando de lint.
- `CHANGELOG.md`: entrada em "Não lançado".

## Decisões visuais registradas neste template

- **Uma única elevação** para todos os cartões. Correção de uma versão que
  tinha 3 sombras diferentes convivendo — a revisão visual apontou que
  quebrava a sensação de sistema coeso.
- **SVG inline, nunca emoji** (`stroke="currentColor"`, herda o tema).
- **Um único breakpoint** (860px). Cada ponto extra é mais um estado para
  manter e regredir.
- **Landing sempre clara**, mesmo com tema escuro na área autenticada:
  material institucional prioriza consistência de apresentação.
- **Nenhum número não medido na interface.** Uma versão anterior exibia
  "400+ sessões" e "<30ms" sem medição; foi removida.
