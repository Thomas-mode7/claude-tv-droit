from piste import sources as S

def test_pick_version_by_date():
    v = [{"id": "old", "dateDebut": -5231606400000, "dateFin": 1475280000000},
         {"id": "new", "dateDebut": 1475280000000, "dateFin": 32472144000000}]
    assert S.pick_version(v, S.to_ms("2010-01-01"))["id"] == "old"
    assert S.pick_version(v, S.to_ms("2016-10-01"))["id"] == "new"   # bascule le jour même
    assert S.pick_version(v, S.to_ms("2030-01-01"))["id"] == "new"
    assert S.pick_version(v, S.to_ms("1800-01-01")) is None          # avant 1804

def test_dates():
    assert S.ms_to_date(1475280000000) == "2016-10-01"
    assert S.ms_to_date(32472144000000) is None  # "sans fin"
    assert S.ms_to_date(None) is None

def test_clean_and_urls():
    assert S.clean("a<br/>b &amp; <mark>c</mark>") == "a\nb & c"
    assert S.url_legifrance("LEGIARTI000032041571").endswith("codes/article_lc/LEGIARTI000032041571")
    assert "/ceta/id/" in S.url_legifrance("CETATEXT1") and S.url_legifrance(None) is None

def test_bad_params_rejected():
    import pytest
    with pytest.raises(S.PisteError): S.rechercher_texte("x", fond="inconnu")
    with pytest.raises(S.PisteError): S.rechercher_jurisprudence("x", juridiction="inconnue")
