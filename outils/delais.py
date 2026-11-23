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
import calendar
import datetime as dt
import json

JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


def paques(annee: int) -> dt.date:
    """Dimanche de Pâques (algorithme grégorien de Meeus/Jones/Butcher)."""
    a, b, c = annee % 19, annee // 100, annee % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mois = (h + l - 7 * m + 114) // 31
    jour = (h + l - 7 * m + 114) % 31 + 1
    return dt.date(annee, mois, jour)


def jours_feries(annee: int, alsace_moselle: bool = False) -> dict[dt.date, str]:
    p = paques(annee)
    f = {
        dt.date(annee, 1, 1): "1er janvier",
        p + dt.timedelta(days=1): "lundi de Pâques",
        dt.date(annee, 5, 1): "1er mai",
        dt.date(annee, 5, 8): "8 mai",
        p + dt.timedelta(days=39): "Ascension",
        p + dt.timedelta(days=50): "lundi de Pentecôte",
        dt.date(annee, 7, 14): "14 juillet",
        dt.date(annee, 8, 15): "Assomption",
        dt.date(annee, 11, 1): "Toussaint",
        dt.date(annee, 11, 11): "11 novembre",
        dt.date(annee, 12, 25): "Noël",
    }
    if alsace_moselle:
        f[p - dt.timedelta(days=2)] = "Vendredi saint (Alsace-Moselle, communes avec temple protestant ou église mixte)"
        f[dt.date(annee, 12, 26)] = "second jour de Noël (Alsace-Moselle)"
    return f


def ajouter_mois(d: dt.date, n: int) -> dt.date:
    """Même quantième n mois plus tard ; à défaut, dernier jour du mois (art. 641 al. 2)."""
    m = d.month - 1 + n
    a, m = d.year + m // 12, m % 12 + 1
    return dt.date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


def calculer(depart: dt.date, jours: int = 0, mois: int = 0, annees: int = 0,
             distance: str | None = None, alsace_moselle: bool = False) -> dict:
    if not (jours or mois or annees):
        raise ValueError("indiquer une durée (jours, mois ou années)")
    augmentation = {None: 0, "metropole": 0, "outre-mer": 1, "etranger": 2}[distance]
    total_mois = annees * 12 + mois + augmentation
    brut = ajouter_mois(depart, total_mois) if total_mois else depart
    brut += dt.timedelta(days=jours)  # mois d'abord, puis jours (art. 641 al. 3)
    fin, reports = brut, []
    while True:
        feries = jours_feries(fin.year, alsace_moselle)
        if fin.weekday() >= 5:
            reports.append(f"{fin.isoformat()} : {JOURS[fin.weekday()]}")
        elif fin in feries:
            reports.append(f"{fin.isoformat()} : {feries[fin]}")
        else:
            break
        fin += dt.timedelta(days=1)
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
