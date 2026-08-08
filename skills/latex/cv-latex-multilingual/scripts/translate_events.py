#!/usr/bin/env python3
"""Traduz os nomes de eventos/congressos em spanish.tex e french.tex.

Uso:  python3 scripts/translate_events.py [DIR_DO_CV]
  (default: /home/pedro/Repositorios/pessoal/cv)

Aplica substituicoes EXATAS (dict abaixo). IMPORTANTE:
- Rodar DENTRO do `terminal` (nao via execute_code/hermes_tools), pois
  write_file de hermes_tools em execute_code NAO persiste no disco.
- As strings-alvo EM ES/FR ja tem substituicoes parciais do translate_cv.py
  (Brazilian->Bresilienne/Brasilian, Computer Engineering->Ingenieria Informatica/
  Ingenierie Informatique). Por isso os dicts usam as strings EXATAS do arquivo,
  nao as do ingles.
- Usa apstrofo tipografico U+2019 (') nos titulos FR.

Ajuste os dicts conforme o conteudo corrente do CV (rode `grep` primeiro para
pegar as strings exatas). O script reporta quaisquer alvos nao encontrados.
"""
import io, sys, os

BASE = sys.argv[1] if len(sys.argv) > 1 else "/home/pedro/Repositorios/pessoal/cv"

# Espanhol: titulos exatos ATUAIS no arquivo (pos-translate_cv.py)
subs_es = {
    "21st Brazilian Science and Engineering Fair": "XXI Feria Brasile\u00f1a de Ciencia e Ingenier\u00eda",
    "40th International Science and Technology Fair": "XL Feria Internacional de Ciencia y Tecnolog\u00eda",
    "IX Brazilian Science Initiation Fair": "IX Feria Brasile\u00f1a de Iniciaci\u00f3n Cient\u00edfica",
    "XVI Scientific and Technological Exhibition of the A\u00e7a\u00ed Institute": "XVI Exposici\u00f3n Cient\u00edfica y Tecnol\u00f3gica del Instituto A\u00e7a\u00ed",
    "XV Scientific and Technological Initiation Congress and IX Fluminense Congress of Postgraduate Studies": "XV Congreso de Iniciaci\u00f3n Cient\u00edfica y Tecnol\u00f3gica y IX Congreso Fluminense de Posgrado",
    "XVI Scientific and Technological Initiation Congress and X Fluminense Congress of Postgraduate Studies": "XVI Congreso de Iniciaci\u00f3n Cient\u00edfica y Tecnol\u00f3gica y X Congreso Fluminense de Posgrado",
    "XLVIII Annual Meeting of the Brazilian Astronomical Society": "XLVIII Reuni\u00f3n Anual de la Sociedad Astron\u00f3mica Brasile\u00f1a",
    "XVII  Scientific and Technological Initiation Congress and XI Fluminense Congress of Postgraduate Studies": "XVII Congreso de Iniciaci\u00f3n Cient\u00edfica y Tecnol\u00f3gica y XI Congreso Fluminense de Posgrado",
    "78\u00aa Annual Meeting of Brazilian Society to Science Progress": "78\u00aa Reuni\u00f3n Anual de la Sociedad Brasile\u00f1a para el Progreso de la Ciencia",
    "Winter School of Astrophysics": "Escuela de Invierno de Astrof\u00edsica",
    "XLIX Annual Meeting of the Brazilian Astronomical Society": "XLIX Reuni\u00f3n Anual de la Sociedad Astron\u00f3mica Brasile\u00f1a",
    "Teaching, Research and Extension Congress (CONEPE)": "Congreso de Ense\u00f1anza, Investigaci\u00f3n y Extensi\u00f3n (CONEPE)",
    "VIII Knowledge Showcase and I Job Fair": "VIII Muestra del Saber y I Feria de Empleo",
    "IX Knowledge Showcase and II Job Fair": "IX Muestra del Saber y II Feria de Empleo",
    "I Week of Ingenier\u00eda Inform\u00e1tica and Management": "I Semana de Ingenier\u00eda Inform\u00e1tica y Gesti\u00f3n",
    "X Knowledge Showcase and III Job Fair": "X Muestra del Saber y III Feria de Empleo",
    "II Week of Ingenier\u00eda Inform\u00e1tica and Management": "II Semana de Ingenier\u00eda Inform\u00e1tica y Gesti\u00f3n",
    "XI Knowledge Showcase and IV Job Fair": "XI Muestra del Saber y IV Feria de Empleo",
    "III Week of Ingenier\u00eda Inform\u00e1tica and Management": "III Semana de Ingenier\u00eda Inform\u00e1tica y Gesti\u00f3n",
    "XII Knowledge Showcase and V Job Fair": "XII Muestra del Saber y V Feria de Empleo",
    "IV Week of Ingenier\u00eda Inform\u00e1tica and Management": "IV Semana de Ingenier\u00eda Inform\u00e1tica y Gesti\u00f3n",
}

# Frances: titulos exatos ATUAIS no arquivo (pos-translate_cv.py, com Bresilienne/Ingenierie)
subs_fr = {
    "21st Br\u00e9silienne Science and Engineering Fair": "XXIe Foire Br\u00e9silienne de Science et Ing\u00e9nierie",
    "40th International Science and Technology Fair": "XLe",  # placeholder; substituir abaixo
    "IX Br\u00e9silienne Science Initiation Fair": "IXe Foire Br\u00e9silienne d\u2019Initiation Scientifique",
    "XVI Scientific and Technological Exhibition of the A\u00e7a\u00ed Institute": "XVIe Exposition Scientifique et Technologique de l\u2019Institut A\u00e7a\u00ed",
    "XV Scientific and Technological Initiation Congress and IX Fluminense Congress of Postgraduate Studies": "XVe Congr\u00e8s d\u2019Initiation Scientifique et Technologique et IXe Congr\u00e8s Fluminense d\u2019\u00c9tudes Sup\u00e9rieures",
    "XVI Scientific and Technological Initiation Congress and X Fluminense Congress of Postgraduate Studies": "XVIe Congr\u00e8s d\u2019Initiation Scientifique et Technologique et Xe Congr\u00e8s Fluminense d\u2019\u00c9tudes Sup\u00e9rieures",
    "XLVIII Annual Meeting of the Br\u00e9silienne Astronomical Society": "XLVIIIe R\u00e9union Annuelle de la Soci\u00e9t\u00e9 Astronomique Br\u00e9silienne",
    "XVII  Scientific and Technological Initiation Congress and XI Fluminense Congress of Postgraduate Studies": "XVIIe Congr\u00e8s d\u2019Initiation Scientifique et Technologique et XIe Congr\u00e8s Fluminense d\u2019\u00c9tudes Sup\u00e9rieures",
    "78\u00aa Annual Meeting of Br\u00e9silienne Society to Science Progress": "78e R\u00e9union Annuelle de la Soci\u00e9t\u00e9 Br\u00e9silienne pour le Progr\u00e8s de la Science",
    "Winter School of Astrophysics": "\u00c9cole d\u2019Hiver d\u2019Astrophysique",
    "XLIX Annual Meeting of the Br\u00e9silienne Astronomical Society": "XLIXe R\u00e9union Annuelle de la Soci\u00e9t\u00e9 Astronomique Br\u00e9silienne",
    "Teaching, Research and Extension Congress (CONEPE)": "Congr\u00e8s d\u2019Enseignement, Recherche et Extension (CONEPE)",
    "VIII Knowledge Showcase and I Job Fair": "VIIIe Exposition du Savoir et I\u00e8re Foire de l\u2019Emploi",
    "IX Knowledge Showcase and II Job Fair": "IXe Exposition du Savoir et IIe Foire de l\u2019Emploi",
    "I Week of Ing\u00e9nierie Informatique and Management": "I\u00e8re Semaine d\u2019Ing\u00e9nierie Informatique et de Gestion",
    "X Knowledge Showcase and III Job Fair": "Xe Exposition du Savoir et IIIe Foire de l\u2019Emploi",
    "II Week of Ing\u00e9nierie Informatique and Management": "IIe Semaine d\u2019Ing\u00e9nierie Informatique et de Gestion",
    "XI Knowledge Showcase and IV Job Fair": "XIe Exposition du Savoir et IVe Foire de l\u2019Emploi",
    "III Week of Ing\u00e9nierie Informatique and Management": "IIIe Semaine d\u2019Ing\u00e9nierie Informatique et de Gestion",
    "XII Knowledge Showcase and V Job Fair": "XIIe Exposition du Savoir et Ve Foire de l\u2019Emploi",
    "IV Week of Ing\u00e9nierie Informatique and Management": "IVe Semaine d\u2019Ing\u00e9nierie Informatique et de Gestion",
}
# corrigir placeholder do item 40th
subs_fr["40th International Science and Technology Fair"] = "XLe Foire Internationale de Science et Technologie"


def apply(path, subs):
    with io.open(path, encoding="utf-8") as f:
        txt = f.read()
    missing = []
    for old, new in subs.items():
        if old in txt:
            txt = txt.replace(old, new)
        else:
            missing.append(old)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(txt)
    return missing


if __name__ == "__main__":
    print("ES missing:", apply(os.path.join(BASE, "spanish.tex"), subs_es))
    print("FR missing:", apply(os.path.join(BASE, "french.tex"), subs_fr))
    print("DONE — rode `make spanishCV frenchCV` e verifique com verify_cv_pdfs.py")
