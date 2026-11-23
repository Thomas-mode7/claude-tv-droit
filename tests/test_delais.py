import datetime as dt
from outils.delais import calculer, paques, ajouter_mois

D = dt.date.fromisoformat

def test_paques():
    assert paques(2026) == D("2026-04-05") and paques(2024) == D("2024-03-31") and paques(2027) == D("2027-03-28")

def test_mois_dernier_jour_et_samedi():
    # 31 janv. + 1 mois -> 28 févr. 2026 (pas de 31) = samedi -> lundi 2 mars
    r = calculer(D("2026-01-31"), mois=1)
    assert r["echeance_theorique"] == "2026-02-28" and r["echeance"] == "2026-03-02"

def test_jours_depart_non_compte():
    assert calculer(D("2026-06-01"), jours=15)["echeance"] == "2026-06-16"  # mardi

def test_ascension():
    # 14 avril + 1 mois = jeudi 14 mai 2026, Ascension -> vendredi 15 mai
    assert calculer(D("2026-04-14"), mois=1)["echeance"] == "2026-05-15"

def test_noel_alsace():
    r = calculer(D("2026-12-10"), jours=15, alsace_moselle=True)  # 25 déc. ven., 26 sam. -> lundi 28
    assert r["echeance"] == "2026-12-28" and len(r["reports_art_642"]) == 3

def test_distance_et_mois_puis_jours():
    assert calculer(D("2026-03-15"), mois=1, distance="etranger")["echeance_theorique"] == "2026-06-15"
    assert calculer(D("2026-01-31"), mois=1, jours=2)["echeance_theorique"] == "2026-03-02"

def test_ajouter_mois_fin_annee():
    assert ajouter_mois(D("2026-12-31"), 2) == D("2027-02-28")
