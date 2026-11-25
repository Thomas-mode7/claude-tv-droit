"""Briques communes de computation des délais : jours fériés, ajout de mois, report, délais en heures.

Fériés : C. trav. L3133-1 (LEGIARTI000033020901) ; Alsace-Moselle L3134-13 (LEGIARTI000006902635).
"""
from __future__ import annotations

import calendar
import datetime as dt

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
    """Même quantième n mois plus tard ; à défaut, dernier jour du mois."""
    m = d.month - 1 + n
    a, m = d.year + m // 12, m % 12 + 1
    return dt.date(a, m, min(d.day, calendar.monthrange(a, m)[1]))


def ajouter_annees(d: dt.date, n: int) -> dt.date:
    return ajouter_mois(d, 12 * n)


def reporter(d: dt.date, alsace_moselle: bool = False) -> tuple[dt.date, list[str]]:
    """Report au premier jour ouvrable si samedi, dimanche ou jour férié."""
    reports = []
    while True:
        feries = jours_feries(d.year, alsace_moselle)
        if d.weekday() >= 5:
            reports.append(f"{d.isoformat()} : {JOURS[d.weekday()]}")
        elif d in feries:
            reports.append(f"{d.isoformat()} : {feries[d]}")
        else:
            return d, reports
        d += dt.timedelta(days=1)


def echeance(depart: dt.date, jours: int = 0, mois: int = 0, annees: int = 0, franc: bool = False,
             report: bool = True, alsace_moselle: bool = False) -> dict:
    """Échéance générique.

    Non franc : le jour de départ ne compte pas ; mois/années au même quantième (à défaut dernier jour du mois).
    Franc : en plus, le dernier jour est le lendemain de l'échéance non franche.
    """
    brut = ajouter_mois(depart, annees * 12 + mois) if (mois or annees) else depart
    brut += dt.timedelta(days=jours)
    if franc:
        brut += dt.timedelta(days=1)
    fin, reports = reporter(brut, alsace_moselle) if report else (brut, [])
    return {"echeance_theorique": brut.isoformat(), "reports": reports, "echeance": fin.isoformat(),
            "jour": JOURS[fin.weekday()], "expire_a": "24h00"}


def echeance_heures(notification: dt.datetime, heures: int) -> dict:
    """Délai décompté d'heure à heure, sans report."""
    fin = notification + dt.timedelta(hours=heures)
    return {"echeance_theorique": fin.isoformat(timespec="minutes"), "reports": [],
            "echeance": fin.isoformat(timespec="minutes"), "jour": JOURS[fin.weekday()],
            "expire_a": fin.strftime("%Hh%M")}
