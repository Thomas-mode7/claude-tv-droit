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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def calculer_delai(point_de_depart: str, jours: int = 0, mois: int = 0, annees: int = 0,
                   distance: str | None = None, alsace_moselle: bool = False) -> dict:
    """Échéance d'un délai de procédure civile selon les art. 640 à 643 CPC (calcul déterministe).

    point_de_depart : AAAA-MM-JJ (acte, événement, décision ou notification qui fait courir le délai).
    jours / mois / annees : durée du délai (ex. appel en matière contentieuse : mois=1).
    distance : metropole | outre-mer | etranger (augmentation de l'art. 643).
    alsace_moselle : ajoute le Vendredi saint et le 26 décembre.
    Reporte au premier jour ouvrable si l'échéance tombe un samedi, dimanche ou jour férié.
    """
    import datetime as dt
    from outils.delais import calculer
    return calculer(dt.date.fromisoformat(point_de_depart), jours, mois, annees, distance, alsace_moselle)


CALC = ToolAnnotations(readOnlyHint=True, openWorldHint=False)


@mcp.tool(annotations=CALC)
def calculer_delai_administratif(recours: str, point_de_depart: str, heure: str | None = None,
                                 distance: str | None = None, alsace_moselle: bool = False,
                                 decision_implicite: bool = False) -> dict:
    """Échéance d'un délai de recours en contentieux administratif, y compris le contentieux des étrangers.

    recours : recours_contentieux | appel | cassation | etrangers_un_mois (R911-1) | etrangers_sept_jours (L921-1) |
              etrangers_48_heures (L921-2 / R921-2-1) | retention_cinq_jours | dublin_retention_sept_jours | cnda |
              jld_retention_96_heures.
    point_de_depart : AAAA-MM-JJ, date de notification ou de publication (ou de réception de la demande si decision_implicite).
    heure : HH:MM de la notification, obligatoire pour les délais en heures.
    distance : outre-mer | etranger (augmentation de l'art. R421-7 CJA, recours de R421-1 seulement).
    Applique la règle des délais francs (CE, avis, 9 juin 2026, n° 512314) et le report au premier jour ouvrable ;
    délais en heures décomptés d'heure à heure sans report.
    """
    from outils.delais_admin import calculer_admin
    return calculer_admin(recours, point_de_depart, heure, distance, alsace_moselle, decision_implicite)


@mcp.tool(annotations=CALC)
def calculer_delai_penal(procedure: str, point_de_depart: str, reside_hors_metropole: bool = False,
                         alsace_moselle: bool = False) -> dict:
    """Échéance d'un délai de procédure pénale (report au premier jour ouvrable, art. 801 CPP).

    procedure : appel_correctionnel | appel_incident | appel_procureur_general | appel_assises |
                appel_ordonnance_instruction | opposition | pourvoi.
    point_de_depart : AAAA-MM-JJ (prononcé, notification ou signification selon le cas).
    reside_hors_metropole : pour l'opposition (1 mois au lieu de 10 jours).
    Pourvoi : 10 jours francs pour les décisions prononcées depuis le 30 septembre 2024, 5 jours francs avant.
    """
    from outils.delais_penal import calculer_procedure_penale
    return calculer_procedure_penale(procedure, point_de_depart, reside_hors_metropole, alsace_moselle)


@mcp.tool(annotations=CALC)
def calculer_prescription_penale(type_prescription: str, categorie: str, date: str,
                                 dernier_acte_interruptif: str | None = None, date_apparition: str | None = None,
                                 duree_speciale_annees: int | None = None, point_de_depart_special: str | None = None,
                                 date_reference: str | None = None) -> dict:
    """Prescription pénale de droit commun.

    type_prescription : action_publique | peine.
    categorie : crime | delit | contravention.
    date : date de l'infraction (action_publique) ou date à laquelle la condamnation est devenue définitive (peine).
    dernier_acte_interruptif : AAAA-MM-JJ (art. 9-2 CPP, action publique).
    date_apparition : infraction occulte ou dissimulée (art. 9-1 CPP), avec délai butoir.
    duree_speciale_annees / point_de_depart_special : régimes spéciaux, après vérification du texte (ex. mineurs victimes).
    Gère la réforme du 1er mars 2017 (art. 112-2 4° C. pén.). Ne gère pas les suspensions.
    """
    from outils.delais_penal import calculer_prescription_action_publique, calculer_prescription_peine
    if type_prescription == "peine":
        return calculer_prescription_peine(categorie, date, date_reference)
    if type_prescription != "action_publique":
        raise ValueError("type_prescription : action_publique | peine")
    return calculer_prescription_action_publique(categorie, date, dernier_acte_interruptif, date_apparition,
                                                 duree_speciale_annees, point_de_depart_special, date_reference)


if __name__ == "__main__":
    mcp.run()
