"""Calcul des délais de procédure civile (art. 640 à 643 CPC).

Règles (textes vérifiés sur Légifrance, version en vigueur au 2026-11-23) :
- art. 640 (LEGIARTI000006411001) : le délai a pour origine l'acte, l'événement, la décision ou la notification.
- art. 641 (LEGIARTI000006411002) : en jours, le jour de départ ne compte pas ; en mois/années, expiration
  au même quantième, à défaut le dernier jour du mois ; mois et jours : mois d'abord, puis jours.
- art. 642 (LEGIARTI000006411003) : expiration à 24h ; samedi, dimanche, jour férié ou chômé -> premier jour ouvrable suivant.
- art. 643 (LEGIARTI000034747123) : +1 mois (outre-mer) / +2 mois (étranger) pour comparution, appel, opposition,
  tierce opposition (586 al. 3), révision et pourvoi, devant une juridiction de métropole.
Jours fériés : C. trav. L3133-1 (LEGIARTI000033020901) ; Alsace-Moselle L3134-13 (LEGIARTI000006902635).

Usage :
  python3 -m outils.delais 2026-01-31 --mois 1
  python3 -m outils.delais 2026-12-10 --jours 15 --alsace-moselle
  python3 -m outils.delais 2026-03-15 --mois 2 --distance etranger
"""
from __future__ import annotations

import argparse
import datetime as dt
import json

from .calendrier import JOURS, ajouter_mois, jours_feries, paques, reporter  # noqa: F401  (réexport)


def calculer(depart: dt.date, jours: int = 0, mois: int = 0, annees: int = 0,
             distance: str | None = None, alsace_moselle: bool = False) -> dict:
    if not (jours or mois or annees):
        raise ValueError("indiquer une durée (jours, mois ou années)")
    augmentation = {None: 0, "metropole": 0, "outre-mer": 1, "etranger": 2}[distance]
    total_mois = annees * 12 + mois + augmentation
    brut = ajouter_mois(depart, total_mois) if total_mois else depart
    brut += dt.timedelta(days=jours)  # mois d'abord, puis jours (art. 641 al. 3)
    fin, reports = reporter(brut, alsace_moselle)
    return {
        "point_de_depart": depart.isoformat(),
        "duree": {"annees": annees, "mois": mois, "jours": jours},
        "augmentation_distance_mois": augmentation,
        "echeance_theorique": brut.isoformat(),
        "reports_art_642": reports,
        "echeance": fin.isoformat(),
        "jour": JOURS[fin.weekday()],
        "expire_a": "24h00 (art. 642 al. 1)",
        "avertissements": [
            "Vérifier le point de départ (notification régulière ? art. 528 CPC) et les délais spéciaux de la matière.",
            "Les jours chômés locaux autres que les fêtes légales ne sont pas pris en compte.",
        ] + (["Augmentation art. 643 : applicable seulement aux délais qu'il énumère, devant une juridiction de métropole."]
             if augmentation else []),
    }


def main():
    ap = argparse.ArgumentParser(description="Calcul de délai de procédure civile (art. 640-643 CPC)")
    ap.add_argument("depart", help="date de l'acte/notification, AAAA-MM-JJ")
    ap.add_argument("--jours", type=int, default=0)
    ap.add_argument("--mois", type=int, default=0)
    ap.add_argument("--annees", type=int, default=0)
    ap.add_argument("--distance", choices=["metropole", "outre-mer", "etranger"])
    ap.add_argument("--alsace-moselle", action="store_true")
    a = ap.parse_args()
    r = calculer(dt.date.fromisoformat(a.depart), a.jours, a.mois, a.annees, a.distance, a.alsace_moselle)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
