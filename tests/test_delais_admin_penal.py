import pytest
from outils.delais_admin import calculer_admin
from outils.delais_penal import (calculer_procedure_penale, calculer_prescription_action_publique,
                                 calculer_prescription_peine)

# --- administratif -------------------------------------------------------------
def test_ce_508820_sept_jours_franc():
    # CE, 10 août 2026, n° 508820 : notification le 18 avril 2025, délai expirant le lundi 28 avril 2025
    r = calculer_admin("etrangers_sept_jours", "2025-04-18")
    assert r["echeance_theorique"] == "2025-04-26" and r["echeance"] == "2025-04-28"

def test_recours_contentieux_franc():
    assert calculer_admin("recours_contentieux", "2026-01-03")["echeance"] == "2026-03-04"

def test_distance_r421_7():
    assert calculer_admin("recours_contentieux", "2026-01-03", distance="etranger")["echeance_theorique"] == "2026-05-04"
    r = calculer_admin("appel", "2026-01-03", distance="etranger")
    assert r["augmentation_distance_mois"] == 0 and any("R421-7" in a for a in r["avertissements"])

def test_decision_implicite():
    r = calculer_admin("recours_contentieux", "2026-01-15", decision_implicite=True)
    assert r["naissance_decision_implicite"] == "2026-03-15" and r["echeance"] == "2026-05-18"  # 16 mai sam. -> lun. 18

def test_48h_heure_a_heure_sans_report():
    # CAA Lyon, 9 janv. 2020, 19LY00133 : délai expirant le 9 déc. 2018 à 18h30
    r = calculer_admin("etrangers_48_heures", "2018-12-07", heure="18:30")
    assert r["echeance"] == "2018-12-09T18:30" and r["jour"] == "dimanche" and r["reports"] == []
    with pytest.raises(ValueError):
        calculer_admin("etrangers_48_heures", "2026-11-20")

def test_delai_incertain_prudent():
    r = calculer_admin("retention_cinq_jours", "2026-11-20")  # vendredi
    assert r["echeance"] == "2026-11-25" and r["echeance_si_delai_franc"] == "2026-11-26"

def test_avertissement_reforme_2026():
    r = calculer_admin("etrangers_un_mois", "2026-05-02")
    assert any("8 juin 2026" in a for a in r["avertissements"])

# --- pénal : procédure ----------------------------------------------------------
def test_appel_correctionnel_report():
    assert calculer_procedure_penale("appel_correctionnel", "2026-11-20")["echeance"] == "2026-11-30"

def test_pourvoi_nouveau_et_ancien():
    r = calculer_procedure_penale("pourvoi", "2026-12-17")
    assert r["duree_jours"] == 10 and r["echeance"] == "2026-12-28"  # 27 = dimanche
    r = calculer_procedure_penale("pourvoi", "2024-06-03")
    assert r["duree_jours"] == 5 and r["echeance"] == "2024-06-10"   # 8 = samedi

def test_opposition():
    assert calculer_procedure_penale("opposition", "2026-03-02")["echeance"] == "2026-03-12"
    assert calculer_procedure_penale("opposition", "2026-03-02", reside_hors_metropole=True)["echeance"] == "2026-04-02"

# --- pénal : prescription -------------------------------------------------------
def test_prescription_delit_recent_et_interruption():
    assert calculer_prescription_action_publique("delit", "2020-01-01")["echeance"] == "2026-01-01"
    r = calculer_prescription_action_publique("delit", "2020-01-01", dernier_acte_interruptif="2024-05-05")
    assert r["echeance"] == "2030-05-05"

def test_prescription_transitoire_2017():
    r = calculer_prescription_action_publique("delit", "2015-01-10")   # 3 ans non acquis au 01/03/2017
    assert r["duree_annees"] == 6 and r["echeance"] == "2021-01-10"
    r = calculer_prescription_action_publique("delit", "2013-05-01")   # acquis le 01/05/2016
    assert r["duree_annees"] == 3 and r["echeance"] == "2016-05-01" and r["prescrite"]

def test_prescription_occulte_butoir():
    r = calculer_prescription_action_publique("delit", "2018-01-01", date_apparition="2027-01-01")
    assert r["echeance"] == "2030-01-01"
    with pytest.raises(ValueError):
        calculer_prescription_action_publique("contravention", "2020-01-01", date_apparition="2021-01-01")

def test_prescription_peine():
    r = calculer_prescription_peine("delit", "2020-06-15", date_reference="2026-11-25")
    assert r["echeance"] == "2026-06-15" and r["prescrite"]

def test_alerte_recodification_2029():
    r = calculer_prescription_action_publique("delit", "2024-01-01")  # échéance 2030
    assert any("2025-1091" in a for a in r["avertissements"])
    r = calculer_procedure_penale("appel_correctionnel", "2026-11-20")
    assert not any("2025-1091" in a for a in r["avertissements"])
