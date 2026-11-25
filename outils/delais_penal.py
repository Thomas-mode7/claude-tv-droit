"""Délais de procédure pénale et prescription (action publique, peine).

Sources vérifiées sur Légifrance le 2026-11-25 :
- CPP 801 (LEGIARTI000006578399) : délai de procédure expire le dernier jour à 24h ; samedi, dimanche, férié ou chômé -> premier jour ouvrable.
- CPP 498 (LEGIARTI000021331547) : appel correctionnel, 10 jours à compter du prononcé (ou de la signification dans les cas visés).
- CPP 500 (LEGIARTI000006576759) : appel incident, délai supplémentaire de 5 jours.
- CPP 505 (LEGIARTI000021331544) : appel du procureur général, 20 jours à compter du prononcé.
- CPP 547 (LEGIARTI000006576924) : appel des jugements de police, délais des art. 498 à 500.
- CPP 380-9 (LEGIARTI000044568457) : appel des arrêts de cour d'assises, 10 jours à compter du prononcé.
- CPP 186 (LEGIARTI000048441733) : appel des ordonnances du juge d'instruction, 10 jours après notification ou signification.
- CPP 491 (LEGIARTI000006576719) : opposition, 10 jours (résidence en France métropolitaine) ou 1 mois (hors), après signification à personne.
- CPP 568 (LEGIARTI000048442131, depuis le 2024-09-30) : pourvoi, 10 jours francs après celui du prononcé ;
  version antérieure (LEGIARTI000006576979, 2004-10-01 -> 2024-09-30) : 5 jours francs.
- CPP 7 (LEGIARTI000043409351), 8 (LEGIARTI000049531911), 9 (LEGIARTI000034099775) : 20 ans / 6 ans / 1 an (depuis le 2017-03-01) ;
  versions antérieures : 10 ans (LEGIARTI000024496760), 3 ans (LEGIARTI000029345388), 1 an (LEGIARTI000024496743).
- CPP 9-1 (LEGIARTI000037289466) : infraction occulte ou dissimulée, point de départ reporté, butoir 12 ans (délits) / 30 ans (crimes).
- CPP 9-2 (LEGIARTI000043409311) : interruption, nouveau délai d'une durée égale au délai initial.
- CPP 9-3 (LEGIARTI000034098595) : suspension (obstacle de droit ou de fait insurmontable).
- C. pén. 112-2 4° (LEGIARTI000006417182) : lois de prescription applicables immédiatement lorsque la prescription n'est pas acquise.
- C. pén. 133-2 (LEGIARTI000034099845), 133-3 (LEGIARTI000034099836), 133-4 (LEGIARTI000006417513) :
  prescription des peines 20 ans / 6 ans / 3 ans à compter de la décision définitive.
- Cass. crim., 13 janv. 2015, n° 13-87.188, Bull. (ECLI:FR:CCASS:2015:CR07484) : pourvoi tardif irrecevable, sauf force majeure.
"""
from __future__ import annotations

import datetime as dt

from .calendrier import JOURS, ajouter_annees, echeance

REFORME_PRESCRIPTION = dt.date(2017, 3, 1)
REFORME_POURVOI = dt.date(2024, 9, 30)
RECODIFICATION_CPP = dt.date(2029, 1, 1)
ALERTE_2029 = ("Le code de procédure pénale (partie législative) est réécrit par l'ordonnance n° 2025-1091 du 19 novembre 2025 "
               "à compter du 1er janvier 2029 : les articles cités sont en abrogation différée à cette date. Pour une échéance "
               "ou un acte à partir de 2029, vérifier les nouveaux articles (get_article avec la date utile).")

PROCEDURES = {
    "appel_correctionnel": ("Appel d'un jugement correctionnel ou de police (prévenu, partie civile, procureur)", 10,
                            ["CPP 498 (LEGIARTI000021331547)", "CPP 547 (LEGIARTI000006576924)"],
                            "Point de départ : prononcé du jugement contradictoire ; signification dans les cas de l'art. 498 al. 2."),
    "appel_incident": ("Appel incident après l'appel d'une autre partie", 5, ["CPP 500 (LEGIARTI000006576759)"],
                       "Point de départ : l'appel principal ; s'ajoute aux délais de l'art. 498 (vérifier le décompte exact)."),
    "appel_procureur_general": ("Appel du procureur général contre un jugement de condamnation", 20,
                                ["CPP 505 (LEGIARTI000021331544)"], "Point de départ : prononcé de la décision."),
    "appel_assises": ("Appel d'un arrêt de cour d'assises", 10, ["CPP 380-9 (LEGIARTI000044568457)"],
                      "Point de départ : prononcé de l'arrêt (signification si partie absente non informée)."),
    "appel_ordonnance_instruction": ("Appel d'une ordonnance du juge d'instruction", 10, ["CPP 186 (LEGIARTI000048441733)"],
                                     "Point de départ : notification ou signification de l'ordonnance."),
    "opposition": ("Opposition à un jugement par défaut (signification à personne)", None, ["CPP 491 (LEGIARTI000006576719)"],
                   "10 jours si le prévenu réside en France métropolitaine, 1 mois sinon ; point de départ : signification."),
    "pourvoi": ("Pourvoi en cassation", None, ["CPP 568"],
                "Point de départ : le lendemain du prononcé (ou signification dans les cas de l'art. 568 al. 2)."),
}


def calculer_procedure_penale(procedure: str, point_de_depart: str, reside_hors_metropole: bool = False,
                              alsace_moselle: bool = False) -> dict:
    if procedure not in PROCEDURES:
        raise ValueError(f"procédure inconnue : {procedure} (valeurs : {', '.join(PROCEDURES)})")
    libelle, jours, sources, depart_txt = PROCEDURES[procedure]
    depart = dt.date.fromisoformat(point_de_depart)
    sources = list(sources) + ["CPP 801 (LEGIARTI000006578399)"]
    avert = [depart_txt,
             "La déclaration d'appel ou de pourvoi se fait au greffe, pendant ses heures d'ouverture : un pourvoi tardif est "
             "irrecevable sauf force majeure (Cass. crim., 13 janv. 2015, n° 13-87.188, Bull.)."]
    res = {"procedure": procedure, "libelle": libelle, "point_de_depart": point_de_depart}

    if procedure == "opposition":
        e = echeance(depart, mois=1, alsace_moselle=alsace_moselle) if reside_hors_metropole \
            else echeance(depart, jours=10, alsace_moselle=alsace_moselle)
        res.update(e)
    elif procedure == "pourvoi":
        n = 10 if depart >= REFORME_POURVOI else 5
        sources[0] = ("CPP 568 (LEGIARTI000048442131)" if n == 10 else "CPP 568, version antérieure (LEGIARTI000006576979)")
        prudent = echeance(depart, jours=n, franc=False, alsace_moselle=alsace_moselle)
        franc = echeance(depart, jours=n, franc=True, alsace_moselle=alsace_moselle)
        res.update(prudent)
        res["duree_jours"] = n
        res["echeance_si_jours_francs_exclut_le_dernier_jour"] = franc["echeance"]
        avert.append(f"« {n} jours francs après celui où la décision a été prononcée » : l'outil retient l'échéance prudente "
                     f"(jour du prononcé exclu, {n}e jour inclus) ; l'interprétation excluant aussi le dernier jour donne un jour "
                     "de plus (non vérifié : ne pas s'y fier).")
        if depart < REFORME_POURVOI + dt.timedelta(days=30) and depart >= REFORME_POURVOI - dt.timedelta(days=30):
            avert.append("Décision proche de l'entrée en vigueur de la nouvelle rédaction de l'art. 568 (30 sept. 2024) : "
                         "vérifier les dispositions transitoires.")
    else:
        res.update(echeance(depart, jours=jours, alsace_moselle=alsace_moselle))
    if dt.date.fromisoformat(res["echeance"]) >= RECODIFICATION_CPP:
        avert.append(ALERTE_2029)
    res["sources"] = sources
    res["avertissements"] = avert
    return res


# ----------------------------------------------------------------------------- prescription de l'action publique
DUREES = {  # catégorie -> (avant 2017-03-01, depuis 2017-03-01, butoir infraction occulte)
    "crime": (10, 20, 30),
    "delit": (3, 6, 12),
    "contravention": (1, 1, None),
}
SOURCES_PRESCRIPTION = {
    "crime": ["CPP 7 (LEGIARTI000043409351)", "CPP 7 ancien (LEGIARTI000024496760)"],
    "delit": ["CPP 8 (LEGIARTI000049531911)", "CPP 8 ancien (LEGIARTI000029345388)"],
    "contravention": ["CPP 9 (LEGIARTI000034099775)", "CPP 9 ancien (LEGIARTI000024496743)"],
}


def calculer_prescription_action_publique(categorie: str, date_infraction: str, dernier_acte_interruptif: str | None = None,
                                          date_apparition: str | None = None, duree_speciale_annees: int | None = None,
                                          point_de_depart_special: str | None = None, date_reference: str | None = None) -> dict:
    """Prescription de l'action publique (droit commun).

    categorie : crime | delit | contravention.
    dernier_acte_interruptif : date du dernier acte interruptif (art. 9-2) : un nouveau délai de même durée court.
    date_apparition : infraction occulte ou dissimulée (art. 9-1) : point de départ reporté, dans la limite du délai butoir.
    duree_speciale_annees / point_de_depart_special : régimes spéciaux (ex. infractions sur mineurs : point de départ
        à la majorité, 30/20/10 ans ; terrorisme : 30 ans ; presse : 3 mois…) à fournir après vérification du texte.
    """
    if categorie not in DUREES:
        raise ValueError("categorie : crime | delit | contravention")
    ancien, nouveau, butoir = DUREES[categorie]
    infraction = dt.date.fromisoformat(date_infraction)
    ref = dt.date.fromisoformat(date_reference) if date_reference else dt.date.today()
    sources = list(SOURCES_PRESCRIPTION[categorie])
    avert, etapes = [], []

    depart = dt.date.fromisoformat(point_de_depart_special) if point_de_depart_special else infraction
    if date_apparition:
        if butoir is None:
            raise ValueError("pas de report occulte/dissimulé pour les contraventions (art. 9-1 vise délits et crimes)")
        depart = dt.date.fromisoformat(date_apparition)
        sources.append("CPP 9-1 (LEGIARTI000037289466)")
        etapes.append(f"Infraction occulte/dissimulée : point de départ reporté au {depart.isoformat()} (art. 9-1).")

    if duree_speciale_annees:
        duree = duree_speciale_annees
        etapes.append(f"Durée spéciale retenue : {duree} ans (à justifier par le texte spécial vérifié).")
    elif infraction >= REFORME_PRESCRIPTION:
        duree = nouveau
    else:
        acquise_ancienne = ajouter_annees(depart, ancien)
        if dernier_acte_interruptif and dt.date.fromisoformat(dernier_acte_interruptif) < REFORME_PRESCRIPTION:
            acquise_ancienne = ajouter_annees(dt.date.fromisoformat(dernier_acte_interruptif), ancien)
        sources.append("C. pén. 112-2 4° (LEGIARTI000006417182)")
        if acquise_ancienne < REFORME_PRESCRIPTION:
            duree = ancien
            etapes.append(f"Faits antérieurs au 1er mars 2017 : prescription de {ancien} an(s) acquise le "
                          f"{acquise_ancienne.isoformat()}, avant l'entrée en vigueur de la loi nouvelle (art. 112-2 4°).")
        else:
            duree = nouveau
            etapes.append(f"Faits antérieurs au 1er mars 2017 mais prescription ({ancien} an(s)) non acquise à cette date : "
                          f"loi nouvelle applicable, durée {nouveau} ans (art. 112-2 4°).")
            avert.append("Vérifier les dispositions transitoires de la loi n° 2017-242 du 27 février 2017 (non vérifié par l'outil).")

    fin = ajouter_annees(depart, duree)
    etapes.append(f"Délai de {duree} an(s) à compter du {depart.isoformat()} : échéance le {fin.isoformat()}.")
    if dernier_acte_interruptif:
        acte = dt.date.fromisoformat(dernier_acte_interruptif)
        if acte > fin:
            avert.append("L'acte « interruptif » est postérieur à l'échéance : il n'a pu interrompre une prescription déjà acquise.")
        else:
            fin = ajouter_annees(acte, duree)
            sources.append("CPP 9-2 (LEGIARTI000043409311)")
            etapes.append(f"Interruption par l'acte du {acte.isoformat()} : nouveau délai de {duree} an(s), échéance le {fin.isoformat()} (art. 9-2).")
    if date_apparition and butoir:
        limite = ajouter_annees(infraction, butoir)
        if fin > limite:
            fin = limite
            etapes.append(f"Délai butoir de {butoir} ans à compter de l'infraction : échéance ramenée au {limite.isoformat()} (art. 9-1).")
        else:
            etapes.append(f"Délai butoir ({butoir} ans, soit le {limite.isoformat()}) non atteint.")

    if fin >= RECODIFICATION_CPP:
        avert.append(ALERTE_2029)
    avert += [
        "Convention de calcul : jour de départ non compté, expiration le jour anniversaire à 24h (« années révolues »). "
        "Report au jour ouvrable (art. 801) non appliqué à la prescription : à vérifier si l'échéance tombe un jour non ouvrable.",
        "Suspension (art. 9-3, obstacle de droit ou de fait insurmontable) non prise en compte : l'ajouter le cas échéant.",
        "Régimes spéciaux non calculés automatiquement (mineurs victimes art. 7 al. 3 et 8, terrorisme, crimes contre l'humanité, "
        "presse, matières fiscales…) : utiliser duree_speciale_annees / point_de_depart_special après vérification du texte.",
    ]
    return {"type": "prescription de l'action publique", "categorie": categorie, "date_infraction": date_infraction,
            "duree_annees": duree, "point_de_depart": depart.isoformat(), "echeance": fin.isoformat(),
            "jour": JOURS[fin.weekday()], "acquise_au": ref.isoformat(), "prescrite": ref > fin,
            "etapes": etapes, "sources": sources, "avertissements": avert}


PEINES = {"crime": (20, "C. pén. 133-2 (LEGIARTI000034099845)"), "delit": (6, "C. pén. 133-3 (LEGIARTI000034099836)"),
          "contravention": (3, "C. pén. 133-4 (LEGIARTI000006417513)")}


def calculer_prescription_peine(categorie: str, date_decision_definitive: str, date_reference: str | None = None) -> dict:
    if categorie not in PEINES:
        raise ValueError("categorie : crime | delit | contravention")
    duree, source = PEINES[categorie]
    d = dt.date.fromisoformat(date_decision_definitive)
    ref = dt.date.fromisoformat(date_reference) if date_reference else dt.date.today()
    fin = ajouter_annees(d, duree)
    avert = ["Régimes spéciaux non calculés : 30 ans pour certains crimes et 20 ans pour certains délits (infractions visées aux "
             "art. 706-16, 706-26, 706-167 CPP et au livre IV bis C. pén.), imprescriptibilité des peines pour les crimes des "
             "art. 211-1 à 212-3 C. pén. : voir les al. 2 et 3 des art. 133-2 et 133-3.",
             "Causes d'interruption et de suspension de la prescription de la peine non prises en compte."]
    if fin >= RECODIFICATION_CPP:
        avert.append(ALERTE_2029 + " À compter de cette date, l'art. 133-2 C. pén. renvoie aux art. L. 5111-4 à "
                     "L. 5111-10 du code de procédure pénale (version future LEGIARTI000052851466).")
    if d < REFORME_PRESCRIPTION:
        avert.append("Décision définitive avant le 1er mars 2017 : vérifier la durée antérieure (version de l'article à cette date).")
    return {"type": "prescription de la peine", "categorie": categorie, "point_de_depart": d.isoformat(),
            "duree_annees": duree, "echeance": fin.isoformat(), "jour": JOURS[fin.weekday()],
            "prescrite": ref > fin, "acquise_au": ref.isoformat(), "sources": [source], "avertissements": avert}
