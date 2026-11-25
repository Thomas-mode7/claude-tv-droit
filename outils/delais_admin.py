"""Délais du contentieux administratif, y compris le contentieux des étrangers (CESEDA).

Sources vérifiées sur Légifrance / Légifrance-JADE le 2026-11-25 (versions en vigueur à cette date) :
- CJA R421-1 (LEGIARTI000039807005) : recours contre une décision dans les deux mois de sa notification ou publication.
- CJA R421-2 (LEGIARTI000039807000) : deux mois à compter de la naissance d'une décision implicite de rejet.
- CJA R421-5 (LEGIARTI000006449946) : délais opposables seulement s'ils sont mentionnés dans la notification.
- CJA R421-7 (LEGIARTI000031180453) : +1 mois outre-mer, +2 mois étranger (recours de R421-1).
- CJA R811-2 (LEGIARTI000026829556) : appel, deux mois. CJA R821-1 (LEGIARTI000006450393) : cassation, deux mois.
- CRPA L231-1 (LEGIARTI000031367611) / L231-4 (LEGIARTI000031367619) : silence de deux mois (acceptation / rejet).
- Règle des délais francs : CE, avis, 9 juin 2026, n° 512314, Lebon (ECLI:FR:CECHR:2026:512314.20260609) : « sauf texte
  contraire, les délais de recours devant les juridictions administratives sont, en principe, des délais francs, leur premier
  jour étant le lendemain du jour de leur déclenchement et leur dernier jour étant le lendemain du jour de leur échéance (...).
  Lorsque ce délai expire un samedi, un dimanche ou un jour férié, un recours reste recevable le premier jour ouvrable suivant. »
  Le même avis juge que le délai de sept jours de l'art. L. 921-1 CESEDA est un délai franc.
- CESEDA R911-1 (LEGIARTI000054213317, depuis le 2026-06-08) : un mois ; pas de prorogation par un recours administratif.
- CESEDA L921-1 (LEGIARTI000049050149) : sept jours.
- CESEDA R921-2-1 (LEGIARTI000054213234, depuis le 2026-06-08) : 48 heures ; 5 jours (rétention, art. 68 §3 règl. 2024/1348) ;
  7 jours (transfert « Dublin » en rétention).
- CESEDA R921-3 (LEGIARTI000054214383) : les délais de L921-1 et R921-2-1 ne sont susceptibles d'aucune prorogation.
- CESEDA R532-10 (LEGIARTI000054215126) : recours CNDA, un mois.
- CESEDA L741-10 (LEGIARTI000052086430) : contestation du placement en rétention devant le juge judiciaire, 96 heures.
- Délais en heures : décompte d'heure à heure, ni franc ni prorogé (CAA Marseille, 7 avril 2022, 21MA04263 ;
  CAA Lyon, 9 janv. 2020, 19LY00133 ; CAA Nancy, 4 févr. 2016, 15NC01871 : jurisprudence des cours, sous l'empire des textes antérieurs).
"""
from __future__ import annotations

import datetime as dt

from .calendrier import ajouter_mois, echeance, echeance_heures

CE_AVIS = "CE, avis, 9 juin 2026, n° 512314, Lebon (ECLI:FR:CECHR:2026:512314.20260609)"
REFORME_2026 = dt.date(2026, 6, 8)

# clé -> (libellé, unité, durée, franc, sources, avertissements propres)
RECOURS = {
    "recours_contentieux": ("Recours pour excès de pouvoir / plein contentieux contre une décision expresse", "mois", 2, True,
                            ["CJA R421-1 (LEGIARTI000039807005)", "CJA R421-5 (LEGIARTI000006449946)", CE_AVIS], []),
    "appel": ("Appel d'un jugement de tribunal administratif", "mois", 2, True,
              ["CJA R811-2 (LEGIARTI000026829556)", CE_AVIS],
              ["Délais spéciaux fréquents (ex. étrangers, urbanisme, référés) : vérifier le texte applicable."]),
    "cassation": ("Pourvoi en cassation devant le Conseil d'État", "mois", 2, True,
                  ["CJA R821-1 (LEGIARTI000006450393)", CE_AVIS], []),
    "etrangers_un_mois": ("Étrangers : recours de droit commun R911-1 (ex. OQTF avec délai de départ volontaire, refus de séjour assorti)",
                          "mois", 1, True, ["CESEDA L614-1 (LEGIARTI000049056408)", "CESEDA L911-1 (LEGIARTI000054213298)",
                                            "CESEDA R911-1 (LEGIARTI000054213317)", CE_AVIS],
                          ["Pas de prorogation par un recours administratif (R911-1 al. 2).",
                           "Si l'étranger est ensuite assigné à résidence ou placé en rétention avant l'échéance, le délai est "
                           "interrompu et un nouveau délai (7 jours ou R921-2-1) court à compter de l'information (R921-1)."]),
    "etrangers_sept_jours": ("Étrangers : procédure L921-1 (assignation à résidence, détention, transfert Dublin…)", "jours", 7, True,
                             ["CESEDA L921-1 (LEGIARTI000049050149)", "CESEDA R921-3 (LEGIARTI000054214383)", CE_AVIS],
                             ["Délai franc et reporté au premier jour ouvrable selon l'avis du Conseil d'État du 9 juin 2026 ; "
                              "auparavant des cours le jugeaient non franc (ex. CAA Lyon, 19 déc. 2024, 24LY03013)."]),
    "etrangers_48_heures": ("Étrangers : procédure L921-2 (rétention, refus d'entrée au titre de l'asile…)", "heures", 48, False,
                            ["CESEDA L921-2 (LEGIARTI000054214355)", "CESEDA R921-2-1 al. 1 (LEGIARTI000054213234)",
                             "CESEDA R921-3 (LEGIARTI000054214383)",
                             "CAA Marseille, 7 avr. 2022, 21MA04263 ; CAA Lyon, 9 janv. 2020, 19LY00133"],
                            ["Décompte d'heure à heure à partir de l'heure de notification, sans report le week-end : "
                             "l'heure exacte de notification est indispensable."]),
    "retention_cinq_jours": ("Étrangers en rétention n'ayant plus le droit de rester (art. 68 §3 règl. UE 2024/1348)", "jours", 5, None,
                             ["CESEDA R921-2-1 al. 2 (LEGIARTI000054213234)", "CESEDA R921-3 (LEGIARTI000054214383)"],
                             ["Caractère franc non tranché à notre connaissance : l'outil retient l'échéance la plus courte "
                              "(non franc, sans report) et indique l'échéance en lecture franche.",
                              "Régime applicable selon la date d'introduction de la demande d'asile (nota décret 2026-456) : vérifier."]),
    "dublin_retention_sept_jours": ("Transfert « Dublin » d'un étranger placé en rétention", "jours", 7, None,
                                    ["CESEDA R921-2-1 al. 3 (LEGIARTI000054213234)", "CESEDA L572-4 (LEGIARTI000049056384)",
                                     "CESEDA R921-3 (LEGIARTI000054214383)"],
                                    ["Caractère franc non tranché pour ce délai réglementaire issu du décret du 6 juin 2026 : "
                                     "échéance prudente = non franc, sans report."]),
    "cnda": ("Recours devant la Cour nationale du droit d'asile contre une décision de l'OFPRA", "mois", 1, None,
             ["CESEDA R532-10 (LEGIARTI000054215126)"],
             ["Délai prescrit à peine d'irrecevabilité ; caractère franc à vérifier : échéance prudente = non franc."]),
    "jld_retention_96_heures": ("Contestation du placement en rétention devant le magistrat du siège du tribunal judiciaire",
                                "heures", 96, False, ["CESEDA L741-10 (LEGIARTI000052086430)"],
                                ["Délai en heures : décompter d'heure à heure à partir de la notification."]),
}

DISTANCE_R421_7 = {"recours_contentieux"}  # R421-7 vise le délai de R421-1


def calculer_admin(recours: str, point_de_depart: str, heure: str | None = None, distance: str | None = None,
                   alsace_moselle: bool = False, decision_implicite: bool = False) -> dict:
    """point_de_depart : date de notification/publication (AAAA-MM-JJ) ; pour decision_implicite=True,
    date de réception de la demande par l'administration. heure : HH:MM (obligatoire pour les délais en heures)."""
    if recours not in RECOURS:
        raise ValueError(f"recours inconnu : {recours} (valeurs : {', '.join(RECOURS)})")
    libelle, unite, duree, franc, sources, avert = RECOURS[recours]
    avert = list(avert)
    depart = dt.date.fromisoformat(point_de_depart)
    res = {"recours": recours, "libelle": libelle, "point_de_depart": point_de_depart}

    if decision_implicite:
        naissance = ajouter_mois(depart, 2)
        res["naissance_decision_implicite"] = naissance.isoformat()
        sources = sources + ["CJA R421-2 (LEGIARTI000039807000)", "CRPA L231-1 (LEGIARTI000031367611)",
                             "CRPA L231-4 (LEGIARTI000031367619)"]
        avert.append("Décision implicite née deux mois après la réception de la demande (sauf délai spécial) ; "
                     "vérifier qu'elle vaut rejet (L231-4) et que l'accusé de réception rend le délai opposable.")
        depart = naissance

    if unite == "heures":
        if not heure:
            raise ValueError("ce délai se compte en heures : indiquer l'heure de notification (HH:MM)")
        notif = dt.datetime.combine(depart, dt.time.fromisoformat(heure))
        res.update(echeance_heures(notif, duree))
    else:
        augmentation = 0
        if distance in ("outre-mer", "etranger"):
            if recours in DISTANCE_R421_7:
                augmentation = 1 if distance == "outre-mer" else 2
                sources = sources + ["CJA R421-7 (LEGIARTI000031180453)"]
            else:
                avert.append("Augmentation de distance non appliquée : R421-7 ne vise que le délai de R421-1 ; "
                             "vérifier un éventuel texte spécial.")
        kw = {"jours": duree} if unite == "jours" else {"mois": duree + augmentation}
        if unite == "jours" and augmentation:
            kw["mois"] = augmentation
        if franc is None:  # incertain : échéance prudente + lecture franche
            prudent = echeance(depart, franc=False, report=False, alsace_moselle=alsace_moselle, **kw)
            lecture_franche = echeance(depart, franc=True, report=True, alsace_moselle=alsace_moselle, **kw)
            res.update(prudent)
            res["echeance_si_delai_franc"] = lecture_franche["echeance"]
        else:
            res.update(echeance(depart, franc=franc, report=True, alsace_moselle=alsace_moselle, **kw))
        res["franc"] = franc
        res["augmentation_distance_mois"] = augmentation

    if depart < REFORME_2026 and recours.startswith(("etrangers", "retention", "dublin")):
        avert.append("Décision notifiée avant le 8 juin 2026 : les délais CESEDA ont été modifiés par les décrets "
                     "n° 2026-455 et 2026-456 ; vérifier la version applicable (get_article avec la date de la décision).")
    avert.append("Délais opposables seulement s'ils sont mentionnés, avec les voies de recours, dans la notification (CJA R421-5).")
    avert.append("Le recours doit être enregistré au greffe (Télérecours) avant l'expiration du délai.")
    res["sources"] = sources
    res["avertissements"] = avert
    return res
