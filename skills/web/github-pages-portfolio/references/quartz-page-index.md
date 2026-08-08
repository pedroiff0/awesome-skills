# Quartz `page` index.md cross-link + per-language CV recipe

Repo: `pedroiff0/page` → live `www.phrandrade.com/<lang>/` (GitHub Pages also at
`pedroiff0.github.io/page` with a 301 → phrandrade). Content lives in
`content/<lang>/index.md` for `pt-br | en | es | fr`.

## 1. Portfolio cross-link callout (all 4 languages)
Insert right after the welcome `> [!info]` callout, before `## 📚 …`:

```markdown
> [!abstract] Conheça também o meu portfólio
> Se você veio do meu **[portfólio de projetos](https://pedroiff0.github.io/webpage/)** (ou quer uma visão rápida de tudo que construí), lá estão todos os meus repositórios do GitHub — públicos e privados — com um *short brief* de cada um, além das bolsas de pesquisa e dos contatos reunidos numa página só. Este site aqui é o conteúdo mais completo (pesquisa, disciplinas, mídia e blog).
```
Translations:
- en: `> [!abstract] Also check out my portfolio` / "If you came from my **[projects portfolio](https://pedroiff0.github.io/webpage/)** (or just want a quick overview of everything I've built), it lists all my GitHub repositories — public and private — each with a *short brief*, plus my research grants and all contacts on a single page. This site here is the full content (research, classes, media and blog)."
- es: `> [!abstract] También visita mi portafolio` / "Si llegaste desde mi **[portafolio de proyectos](https://pedroiff0.github.io/webpage/)** …"
- fr: `> [!abstract] Découvrez aussi mon portfolio` / "Si vous venez de mon **[portfolio de projets](https://pedroiff0.github.io/webpage/)** …"

## 2. Replace the "CV in every language" block with 2 cards (this page's language + repo)
DELETE the bullet list of 4–5 language PDFs AND the `![[assets/curriculo/<x>CV.pdf]]`
viewer. Replace the `### 📄 Currículo…` intro + grid with exactly two cards.

pt-br (other languages swap the PDF path + labels):
```markdown
### 🎓 Currículo & Repositório

Abaixo o meu CV no idioma desta página e o repositório (LaTeX, multilíngue) que o gera:

<div class="cv-cards-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin: 1.75rem 0;">

  <a href="/assets/curriculo/portugueseCV.pdf" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit; display: flex;">
    <div style="background: var(--light); border: 1px solid var(--lightgray); border-radius: 10px; padding: 1.25rem 1.5rem; width: 100%; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.25s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.04);" onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 6px 16px rgba(0,0,0,0.08)';" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 2px 6px rgba(0,0,0,0.04)';">
      <div>
        <div style="font-size: 1.6rem; margin-bottom: 0.75rem; line-height: 1;">🇧🇷</div>
        <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 0.35rem; color: var(--dark);">CV em Português</div>
        <div style="font-size: 0.85rem; color: var(--gray); line-height: 1.4;">Versão em PDF de duas colunas</div>
      </div>
      <div style="margin-top: 1.25rem; font-weight: 600; font-size: 0.85rem; color: var(--tertiary); display: flex; align-items: center; gap: 0.35rem;">
        <span>Baixar / Visualizar PDF</span> <span>↗</span>
      </div>
    </div>
  </a>

  <a href="https://github.com/pedroiff0/curriculo" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit; display: flex;">
    <div style="background: var(--light); border: 1px solid var(--lightgray); border-radius: 10px; padding: 1.25rem 1.5rem; width: 100%; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.25s ease; box-shadow: 0 2px 6px rgba(0,0,0,0.04);" onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 6px 16px rgba(0,0,0,0.08)';" onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 2px 6px rgba(0,0,0,0.04)';">
      <div>
        <div style="font-size: 1.6rem; margin-bottom: 0.75rem; line-height: 1;">📄</div>
        <div style="font-weight: 700; font-size: 1.05rem; margin-bottom: 0.35rem; color: var(--dark);">Repositório do CV</div>
        <div style="font-size: 0.85rem; color: var(--gray); line-height: 1.4;">Código-fonte LaTeX (PT/EN/ES/FR)</div>
      </div>
      <div style="margin-top: 1.25rem; font-weight: 600; font-size: 0.85rem; color: var(--tertiary); display: flex; align-items: center; gap: 0.35rem;">
        <span>Ver no GitHub</span> <span>↗</span>
      </div>
    </div>
  </a>

</div>
```
PDF paths per language: `portugueseCV.pdf` (pt-br), `englishCV.pdf` (en),
`spanishCV.pdf` (es), `frenchCV.pdf` (fr). Repo card link is identical for all four:
`https://github.com/pedroiff0/curriculo`.

## 3. Deploy / verify
See SKILL.md "Deploying edits to a Quartz repo". TL;DR: commit → `git push origin main`
(rebase if rejected) → wait ~2–3 min for Actions build → `curl -m 25` the live URL;
the Varnish CDN may serve a stale copy for ~1 min. Trust `git log --oneline -1` on
`origin/main` if curl times out.
