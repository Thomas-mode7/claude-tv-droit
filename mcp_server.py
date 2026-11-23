"""Serveur MCP « sources juridiques » : Légifrance + Judilibre via PISTE.

Lancement (stdio) : python3 mcp_server.py
Variables requises : PISTE_ENV, PISTE_CLIENT_ID, PISTE_CLIENT_SECRET.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

from piste import sources  # noqa: E402

RO = ToolAnnotations(readOnlyHint=True, openWorldHint=True)

mcp = MCPServer(
    name="sources-juridiques",
    instructions=(
        "Sources officielles du droit français (Légifrance, Judilibre). "
        "Règles : ne citer un article ou une décision qu'après l'avoir obtenu par ces outils ; "
        "toujours donner l'identifiant (LEGIARTI, ECLI, numéro de pourvoi) et l'URL ; "
        "pour un article, demander la version en vigueur à la date des faits (paramètre date)."
    ),
)


@mcp.tool(annotations=RO)
def get_article(code: str, numero: str, date: str | None = None) -> dict:
    """Texte exact d'un article de code, dans la version en vigueur à une date donnée.

    code : nom exact du code, ex. « Code civil », « Code du travail », « Code pénal ».
    numero : numéro de l'article, ex. « 1240 », « L1234-1 », « R. 4127-1 » -> « R4127-1 ».
    date : AAAA-MM-JJ (date des faits). Par défaut : aujourd'hui.
    """
    return sources.get_article(code, numero, date)


@mcp.tool(annotations=RO)
def rechercher_texte(requete: str, fond: str = "codes", date: str | None = None, nb: int = 10) -> list[dict]:
    """Recherche plein texte dans les textes officiels.

    fond : codes | lois_decrets | conventions_collectives | journal_officiel | cnil.
    date : AAAA-MM-JJ pour les versions en vigueur à cette date (codes, lois_decrets).
    nb : nombre de résultats (max 50).
    """
    return sources.rechercher_texte(requete, fond, date, nb)


@mcp.tool(annotations=RO)
def rechercher_jurisprudence(requete: str, juridiction: str = "cassation", date_min: str | None = None,
                             date_max: str | None = None, nb: int = 10,
                             publiees_seulement: bool = False) -> list[dict]:
    """Recherche de décisions de justice.

    juridiction : cassation | appel | premiere_instance (Judilibre) ;
                  administratif (Conseil d'État, CAA, TA) | constitutionnel (Légifrance).
    date_min / date_max : AAAA-MM-JJ.
    publiees_seulement : ne garder que les décisions publiées (Bulletin, Rapport, Lebon…).
    Renvoie les métadonnées et un extrait ; utiliser get_decision pour le texte intégral.
    """
    return sources.rechercher_jurisprudence(requete, juridiction, date_min, date_max, nb, publiees_seulement)


@mcp.tool(annotations=RO)
def get_decision(identifiant: str, max_caracteres: int = 60000) -> dict:
    """Texte intégral et métadonnées d'une décision.

    identifiant : id Judilibre (ex. 607980e59ba5988459c4a365) ou id Légifrance
                  (JURITEXT…, CETATEXT…, CONSTEXT…), tel que renvoyé par rechercher_jurisprudence.
    """
    return sources.get_decision(identifiant, max_caracteres)


if __name__ == "__main__":
    mcp.run()
