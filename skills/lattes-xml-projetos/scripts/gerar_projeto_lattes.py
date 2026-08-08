#!/usr/bin/env python3
"""Gera XML de importacao Lattes contendo apenas itens de bolsa/projetos.

Usa o formato canonico do Lattes (igual ao Lattes_final.xml exportado pelo
site), ou seja:
    CURRICULO-VITAE
      DADOS-GERAIS (atributo NOME-COMPLETO, nao elemento filho)
      ATUACOES-PROFISSIONAIS
        ATUACAO-PROFISSIONAL
          VINCULOS TIPO-DE-VINCULO="Bolsista"
          ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO
            PARTICIPACAO-EM-PROJETO
              PROJETO-DE-PESQUISA ...

IMPORTANTE: a DTD LMPLCurriculo.DTD (versao antiga, 2004-2006) em alguns
diretorios NAO valida esse formato novo (ela nao conhece ATUACOES-PROFISSIONAIS
nem TIPO-DE-VINCULO="Bolsista"). O proprio Lattes_final.xml falha contra ela.
Portanto a validacao correta e so o well-formedness:
    xmllint --noout Lattes_bolsas.xml   # deve sair 0 (sem erros)

Edite a lista PROJETOS abaixo e rode:
    python3 gerar_projeto_lattes.py
Saida: Lattes_bolsas.xml (ISO-8859-1, well-formed).
"""
import html
import sys

REPL = {
    "\u2014": "-", "\u2013": "-", "\u2026": "...",
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2192": "->", "\u2248": "~", "\u00b2": "2", "\u00b9": "1",
    "\u2022": "-", "\u00a0": " ", "\u2009": " ",
    "\u00e7ã": "çã",
}


def clean(s):
    for k, v in REPL.items():
        s = s.replace(k, v)
    # remove qualquer caractere fora de latin-1 (sera trocado por '?' no write)
    return s


def esc(s):
    return html.escape(s, quote=True)


def projeto(p):
    attrs = (f'NOME-DO-PROJETO="{esc(p["nome"])}" NATUREZA="{p["natureza"]}" '
             f'ANO-INICIO="{p["ano_ini"]}" MES-INICIO="{p.get("mes_ini", "")}" '
             f'ANO-FIM="{p["ano_fim"]}" MES-FIM="{p.get("mes_fim", "")}" '
             f'SITUACAO="{p["situacao"]}" '
             f'DESCRICAO-DO-PROJETO="{esc(p["desc"])}"')
    return (f'        <PARTICIPACAO-EM-PROJETO>\n'
            f'          <PROJETO-DE-PESQUISA {attrs}/>\n'
            f'        </PARTICIPACAO-EM-PROJETO>')


# ---------------------------------------------------------------------------
# PROJETOS: edite/adicione conforme necessario.
# natureza: PESQUISA | EXTENSAO | ENSINO  ; situacao: EM_ANDAMENTO | CONCLUIDO
# ano_fim vazio ("") para projetos em andamento.
# ---------------------------------------------------------------------------
PROJETOS = [
    {
        "nome": "Detecção de Anomalias em Estrelas da Via Láctea: Explorando Dados do Gaia e Outros Surveys com Aprendizado de Máquina",
        "natureza": "PESQUISA", "ano_ini": "2024", "mes_ini": "1",
        "ano_fim": "", "mes_fim": "", "situacao": "EM_ANDAMENTO",
        "desc": ("A Via Láctea abriga bilhões de estrelas. Grandes surveys, como o Gaia, "
                 "possuem dados de paralaxes e movimentos próprios. Este projeto aplica "
                 "aprendizado de máquina a dados do Gaia e de outros surveys (Gaia-ESO, "
                 "GALAH, J-PAS/J-PLUS) para detectar medições espúrias, sistemas estelares "
                 "peculiares e detecções inesperadas, voltado a estudantes de iniciação científica."),
    },
    {
        "nome": "Análise de simulações dinâmicas de aglomerados de galáxias em fusão",
        "natureza": "PESQUISA", "ano_ini": "2022", "mes_ini": "9",
        "ano_fim": "2023", "mes_fim": "3", "situacao": "CONCLUIDO",
        "desc": ("Avaliação da acurácia de simulações dinâmicas de aglomerados de galáxias "
                 "em fusão quanto à diferenciação das diversas passagens temporais dos objetos "
                 "em interação pelo centro da colisão, a partir de dados públicos e programação."),
    },
    {
        "nome": "MobFog no IFFMaker",
        "natureza": "EXTENSAO", "ano_ini": "2023", "mes_ini": "8",
        "ano_fim": "2024", "mes_fim": "2", "situacao": "CONCLUIDO",
        "desc": ("Projeto e teste de ogivas e aletas para foguetes didáticos (corpo de garrafa "
                 "PET, bicarbonato e vinagre) por impressão 3D, em parceria entre ensino superior "
                 "e médio técnico, para aumentar o alcance e consolidar metodologias maker."),
    },
    {
        "nome": "Simulando o Impacto de Satélites em Observações Astronômicas",
        "natureza": "PESQUISA", "ano_ini": "2025", "mes_ini": "1",
        "ano_fim": "", "mes_fim": "", "situacao": "EM_ANDAMENTO",
        "desc": ("Iniciação Científica (2025) sob orientação da Dra. Ana Cecília Soja, "
                 "simulando o impacto de constelações de satélites em observações astronômicas ópticas."),
    },
]


def build(projetos):
    blocos = "\n".join(projeto(p) for p in projetos)
    return f'''<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE CURRICULO-VITAE SYSTEM "LMPLCurriculo.DTD">
<CURRICULO-VITAE>
  <DADOS-GERAIS NOME-COMPLETO="Pedro Henrique Rocha de Andrade" PERMISSAO-DE-DIVULGACAO="SIM" SEXO="M" NACIONALIDADE="Brasileira" NOME-EM-CITACOES-BIBLIOGRAFICAS="ANDRADE, P. H. R.">
    <RESUMO-CV TEXTO-RESUMO-CV-RH="Sou estudante de Engenharia de Computação no Instituto Federal Fluminense, com foco em Astrofísica Computacional e Machine Learning."/>
    <ENDERECO>
      <ENDERECO-PROFISSIONAL NOME-DO-ORGANIZADOR="Instituto Federal Fluminense" ENDERECO="Praça da Matriz, 24 - Campos dos Goytacazes - RJ" CEP="28010-460" CODIGO-PAIS="BRA" CODIGO-ESTADO="RJ"/>
    </ENDERECO>
  </DADOS-GERAIS>

  <ATUACOES-PROFISSIONAIS>
    <ATUACAO-PROFISSIONAL>
      <VINCULOS TIPO-DE-VINCULO="Bolsista" ANO-INICIO="2022" MES-INICIO="9" ANO-FIM="" MES-FIM="" FLAG-VINCULO-EMPREGATICIO="NAO"/>
      <ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO>
{blocos}
      </ATIVIDADES-DE-PARTICIPACAO-EM-PROJETO>
    </ATUACAO-PROFISSIONAL>
  </ATUACOES-PROFISSIONAIS>
</CURRICULO-VITAE>
'''


if __name__ == "__main__":
    if not PROJETOS:
        print("Edite a lista PROJETOS no topo do script.", file=sys.stderr)
        sys.exit(2)
    out = build([{k: clean(v) if isinstance(v, str) else v for k, v in p.items()} for p in PROJETOS])
    with open("Lattes_bolsas.xml", "w", encoding="iso-8859-1", errors="replace") as f:
        f.write(out)
    print("Gerado Lattes_bolsas.xml")
