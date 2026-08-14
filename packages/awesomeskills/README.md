# awesomeskills

CLI tools for the [awesome-skills](https://github.com/pedroiff0/awesome-skills) catalog.

## Install

```bash
pip install awesomeskills
# or, from this repo:
pip install ./packages/awesomeskills
```

## Commands

```bash
# Regenerate README.md from skills/**/SKILL.md
awesomeskills index --root .

# Generate the installed-skills inventory from ~/.hermes
awesomeskills catalog
```

Both commands are also importable:

```python
from awesomeskills import gen_index, gen_catalog
gen_index.main(root=".")
gen_catalog.main()
```
