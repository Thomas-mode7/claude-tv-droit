"""Accès normalisé aux sources juridiques (Légifrance + Judilibre).

Chaque fonction renvoie un dict simple, avec toujours : identifiant officiel,
texte verbatim (ou extrait) et URL publique, pour permettre une citation vérifiable.
Chaque appel est journalisé (logs/audit.jsonl).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import time
from pathlib import Path

from .client import Piste, PisteError

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "logs" / "audit.jsonl"
FAR_FUTURE_MS = 32472144000000  # 2999-01-01, "sans date de fin" chez Légifrance

_piste: Piste | None = None


def piste() -> Piste:
    global _piste
    if _piste is None:
        _piste = Piste()
    return _piste


# --------------------------------------------------------------------------- utilitaires
def clean(s: str | None) -> str:
    """HTML -> texte brut lisible."""
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>|</p>|</div>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n\n", s).strip()


def to_ms(date: str | None) -> int:
    """'AAAA-MM-JJ' (ou None = aujourd'hui) -> millisecondes epoch UTC."""
    d = dt.date.fromisoformat(date) if date else dt.date.today()
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp() * 1000)


def ms_to_date(ms) -> str | None:
    if ms in (None, "", 0):
        return None
    ms = int(ms)
    if ms >= FAR_FUTURE_MS:
        return None  # pas de date de fin
    return (dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc) + dt.timedelta(milliseconds=ms)).date().isoformat()


def audit(tool: str, args: dict, result_ids: list[str], error: str | None = None) -> None:
    try:
        AUDIT.parent.mkdir(exist_ok=True)
        with AUDIT.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                                "tool": tool, "args": args, "ids": result_ids, "error": error},
                               ensure_ascii=False) + "\n")
    except OSError:
        pass


def _audited(tool: str, args: dict, fn, ids_of):
    try:
        out = fn()
    except PisteError as e:
        audit(tool, args, [], str(e)[:300])
        raise
    audit(tool, args, ids_of(out))
    return out


def url_legifrance(id_: str | None) -> str | None:
    if not id_:
        return None
    prefix = {"LEGIARTI": "codes/article_lc", "JURITEXT": "juri/id", "CETATEXT": "ceta/id",
              "CONSTEXT": "cons/id", "LEGITEXT": "codes/texte_lc", "JORFTEXT": "jorf/id",
              "KALIARTI": "conv_coll/article", "KALITEXT": "conv_coll/id"}
    for k, v in prefix.items():
        if id_.startswith(k):
            return f"https://www.legifrance.gouv.fr/{v}/{id_}"
    return f"https://www.legifrance.gouv.fr/search/all?query={id_}"


# --------------------------------------------------------------------------- textes
def pick_version(versions: list[dict], date_ms: int) -> dict | None:
    """Version dont [dateDebut, dateFin[ contient la date demandée."""
    for v in versions:
        debut = int(v.get("dateDebut") or -10**15)
        fin = int(v.get("dateFin") or FAR_FUTURE_MS)
        if debut <= date_ms < fin:
            return v
    return None


def get_article(code: str, numero: str, date: str | None = None) -> dict:
    args = {"code": code, "numero": numero, "date": date}

    def run():
        p = piste()
        date_ms = to_ms(date)
        res = p.lf_search_code_article(code, numero, date_ms)
        candidats = []
        for r in res.get("results", []):
            for s in r.get("sections", []):
                for e in s.get("extracts", []):
                    if str(e.get("num", "")).strip() == numero.strip():
                        candidats.append(e["id"])
        if not candidats:
            raise PisteError(f"Article {numero} introuvable dans « {code} » à la date {date or 'du jour'}. "
                             "Vérifiez le nom exact du code (ex. « Code civil », « Code du travail »).")
        art, version = None, None
        for cid in dict.fromkeys(candidats):  # dédoublonné, ordre conservé
            a = p.lf_article(cid)["article"]
            v = pick_version(a.get("articleVersions") or [a], date_ms)
            if v:
                art = a if v["id"] == a["id"] else p.lf_article(v["id"])["article"]
                version = v
                break
        if art is None:
            raise PisteError(f"Aucune version de l'article {numero} n'était en vigueur au {date}.")
        return {
            "source": "Légifrance",
            "code": code,
            "numero": art.get("num"),
            "id": art["id"],
            "etat": art.get("etat"),
            "en_vigueur_du": ms_to_date(art.get("dateDebut")),
            "en_vigueur_jusqu_au": ms_to_date(art.get("dateFin")),
            "date_demandee": date or dt.date.today().isoformat(),
            "texte": clean(art.get("texteHtml") or art.get("texte")),
            "nota": clean(art.get("notaHtml") or art.get("nota")) or None,
            "url": url_legifrance(art["id"]),
            "alerte": ({"ABROGE_DIFF": f"Abrogation différée : texte applicable jusqu'au {ms_to_date(art.get('dateFin'))} "
                                       "exclu ; vérifier le texte qui le remplace (voir autres_versions).",
                        "VIGUEUR_DIFF": "Version future, pas encore en vigueur à la date demandée."}
                       .get(art.get("etat"))),
            "autres_versions": [{"id": v["id"], "etat": v.get("etat"),
                                 "du": ms_to_date(v.get("dateDebut")), "au": ms_to_date(v.get("dateFin"))}
                                for v in (art.get("articleVersions") or []) if v["id"] != art["id"]],
        }

    return _audited("get_article", args, run, lambda o: [o["id"]])


FONDS_TEXTES = {"codes": "CODE_DATE", "lois_decrets": "LODA_DATE", "conventions_collectives": "KALI",
                "journal_officiel": "JORF", "cnil": "CNIL"}


def rechercher_texte(requete: str, fond: str = "codes", date: str | None = None, nb: int = 10) -> list[dict]:
    args = {"requete": requete, "fond": fond, "date": date, "nb": nb}
    if fond not in FONDS_TEXTES:
        raise PisteError(f"fond inconnu : {fond} (valeurs : {', '.join(FONDS_TEXTES)})")

    def run():
        f = FONDS_TEXTES[fond]
        body = {"fond": f, "recherche": {
            "champs": [{"typeChamp": "ALL", "operateur": "ET", "criteres": [
                {"typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP", "valeur": requete, "operateur": "ET"}]}],
            "pageNumber": 1, "pageSize": max(1, min(nb, 50)), "operateur": "ET", "sort": "PERTINENCE",
            "typePagination": "ARTICLE" if f == "CODE_DATE" else "DEFAUT"}}
        if f in ("CODE_DATE", "LODA_DATE"):
            body["recherche"]["filtres"] = [{"facette": "DATE_VERSION", "singleDate": to_ms(date)}]
        res = piste().call("legifrance", "POST", "/search", json=body)
        out = []
        for r in res.get("results", []):
            titre = clean(" > ".join(t.get("title") or "" for t in r.get("titles", []) if t.get("title")))
            pairs = [(s, e) for s in r.get("sections", []) for e in s.get("extracts", [])]
            if pairs:
                for s, e in pairs:
                    out.append({"id": e.get("id"), "titre": titre, "section": clean(s.get("title")) or None,
                                "numero": e.get("num") or e.get("title") or None,
                                "statut": e.get("legalStatus"), "statut_texte": r.get("etat"),
                                "extrait": clean(" ".join(e.get("values") or []))[:500],
                                "url": url_legifrance(e.get("id", ""))})
            else:
                tid = (r.get("titles") or [{}])[0].get("id")
                out.append({"id": tid, "titre": titre, "statut_texte": r.get("etat"),
                            "extrait": clean(" ".join(r.get("text") or []) if isinstance(r.get("text"), list)
                                             else r.get("text"))[:500],
                            "url": url_legifrance(tid)})
        return out[:nb]

    return _audited("rechercher_texte", args, run, lambda o: [x["id"] for x in o])


# --------------------------------------------------------------------------- jurisprudence
JUDILIBRE = {"cassation": ["cc"], "appel": ["ca"], "premiere_instance": ["tj", "tcom", "cph"]}
LEGIFRANCE_JURI = {"administratif": "CETAT", "constitutionnel": "CONSTIT"}
PUBLICATION = {"b": "Bulletin", "r": "Rapport annuel", "l": "Lettre de chambre", "c": "Communiqué", "n": "Non publié"}


def rechercher_jurisprudence(requete: str, juridiction: str = "cassation", date_min: str | None = None,
                             date_max: str | None = None, nb: int = 10, publiees_seulement: bool = False) -> list[dict]:
    args = {"requete": requete, "juridiction": juridiction, "date_min": date_min, "date_max": date_max,
            "nb": nb, "publiees_seulement": publiees_seulement}
    if juridiction not in JUDILIBRE and juridiction not in LEGIFRANCE_JURI:
        raise PisteError(f"juridiction inconnue : {juridiction} "
                         f"(valeurs : {', '.join([*JUDILIBRE, *LEGIFRANCE_JURI])})")

    def run():
        nbx = max(1, min(nb, 50))
        if juridiction in JUDILIBRE:
            params = {"query": requete, "page_size": nbx, "jurisdiction": JUDILIBRE[juridiction],
                      "resolve_references": "true"}
            if date_min:
                params["date_start"] = date_min
            if date_max:
                params["date_end"] = date_max
            if publiees_seulement:
                params["publication"] = ["b", "r", "l", "c"]
            res = piste().call("judilibre", "GET", "/search", params=params)
            return [_judilibre_meta(r) | {"extrait": r.get("summary") or
                                           clean(" … ".join(r.get("highlights", {}).get("text", [])))[:600]}
                    for r in res.get("results", [])]
        fond = LEGIFRANCE_JURI[juridiction]
        body = {"fond": fond, "recherche": {
            "champs": [{"typeChamp": "ALL", "operateur": "ET", "criteres": [
                {"typeRecherche": "TOUS_LES_MOTS_DANS_UN_CHAMP", "valeur": requete, "operateur": "ET"}]}],
            "pageNumber": 1, "pageSize": nbx, "operateur": "ET", "sort": "PERTINENCE", "typePagination": "DEFAUT"}}
        if date_min or date_max:
            body["recherche"]["filtres"] = [{"facette": "DATE_DECISION", "dates": {
                "start": date_min or "1800-01-01", "end": date_max or dt.date.today().isoformat()}}]
        res = piste().call("legifrance", "POST", "/search", json=body)
        out = []
        for r in res.get("results", []):
            t = (r.get("titles") or [{}])[0]
            if publiees_seulement and "Inédit" in t.get("title", ""):
                continue
            out.append({"source": "Légifrance", "id": t.get("id"), "titre": clean(t.get("title")),
                        "extrait": clean(" ".join(r.get("text") or []) if isinstance(r.get("text"), list)
                                         else r.get("text"))[:600] or None,
                        "url": url_legifrance(t.get("id", ""))})
        return out

    return _audited("rechercher_jurisprudence", args, run, lambda o: [x["id"] for x in o])


def _judilibre_meta(r: dict) -> dict:
    return {
        "source": "Judilibre",
        "id": r.get("id"),
        "ecli": r.get("ecli"),
        "juridiction": r.get("jurisdiction"),
        "chambre": r.get("chamber"),
        "numero": r.get("number"),
        "date": r.get("decision_date"),
        "solution": r.get("solution"),
        "publication": [PUBLICATION.get(p, p) for p in (r.get("publication") or [])],
        "themes": r.get("themes") or [],
        "url": f"https://www.courdecassation.fr/decision/{r.get('id')}",
    }


def get_decision(identifiant: str, max_caracteres: int = 60000) -> dict:
    args = {"identifiant": identifiant, "max_caracteres": max_caracteres}

    def run():
        if re.match(r"^(JURITEXT|CETATEXT|CONSTEXT)\d+$", identifiant):
            t = piste().call("legifrance", "POST", "/consult/juri", json={"textId": identifiant})["text"]
            texte = clean(t.get("texteHtml") or t.get("texte"))
            return {"source": "Légifrance", "id": t["id"], "titre": t.get("titre"), "ecli": t.get("ecli"),
                    "juridiction": t.get("juridiction"), "formation": t.get("formation"),
                    "numero": t.get("num") or None, "date": ms_to_date(t.get("dateTexte")),
                    "solution": t.get("solution"), "publication": t.get("publicationRecueil"),
                    "texte": texte[:max_caracteres], "tronque": len(texte) > max_caracteres,
                    "url": url_legifrance(t["id"])}
        d = piste().jl_decision(identifiant)
        texte = d.get("text") or ""
        meta = _judilibre_meta(d)
        meta.update({"sommaire": d.get("summary"), "visa": [v.get("title") for v in d.get("visa") or []],
                     "decision_attaquee": d.get("contested"),
                     "rapprochements": [x.get("title") for x in d.get("rapprochements") or []],
                     "texte": texte[:max_caracteres], "tronque": len(texte) > max_caracteres})
        return meta

    return _audited("get_decision", args, run, lambda o: [o["id"]])
