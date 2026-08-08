# Production patterns (disclaimer + issue watcher)

Two pieces that the quartz-site rollout needed and the base skill omitted.

## A. Auto-disclaimer on every translated page

Append a per-language notice to the END of each machine-translated page (after the
last section, e.g. "Referências e correlatos"), citing the translator mechanism.
Keep it in the page's own language.

```python
DISCLAIMER = {
    "en": (
        "> [!abstract] Automatic translation notice\n"
        "> This page was automatically translated from Portuguese using the "
        "LibreTranslate-based automated translator implemented in "
        "`tools/translate_quartz.py` (it preserves wikilinks, embeds and proper "
        "names via positional splitting). Machine translation may contain "
        "inaccuracies — the original Portuguese version is the authoritative source.\n"
    ),
    "es": (
        "> [!abstract] Aviso de traducción automática\n"
        "> Esta página fue traducida automáticamente del portugués utilizando el "
        "traductor automático basado en LibreTranslate implementado en "
        "`tools/translate_quartz.py` (que preserva wikilinks, embeds y nombres "
        "propios mediante división posicional). Es traducción automática y puede "
        "contener imprecisiones — la versión original en portugués es la fuente "
        "autoritativa.\n"
    ),
    "fr": (
        "> [!abstract] Avis de traduction automatique\n"
        "> Cette page a été traduite automatiquement du portugais à l'aide du "
        "traducteur automatique basé sur LibreTranslate implémenté dans "
        "`tools/translate_quartz.py` (qui préserve les wikilinks, les embeds et "
        "les noms propres par découpage positionnel). Il s'agit d'une traduction "
        "automatique pouvant contenir des inexactitudes — la version portugaise "
        "originale fait foi.\n"
    ),
}

def translate_body(body, target):
    out = "\n".join(translate_line(l, target) for l in body.split("\n"))
    disc = DISCLAIMER.get(target, "")
    if disc:
        out = out.rstrip() + "\n\n" + disc.rstrip() + "\n"
    return out
```

Retrofit onto already-generated pages with `--overwrite`.
