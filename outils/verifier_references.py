"""Vérifie que chaque identifiant LEGIARTI cité dans le dépôt existe et est en vigueur.

Usage : python3 -m outils.verifier_references [fichiers…]  (défaut : skills, outils, docs)
Code de sortie 1 si une référence est introuvable ou n'est plus en vigueur.
"""
import re, sys
from pathlib import Path
from piste.client import Piste, PisteError

ROOT = Path(__file__).resolve().parent.parent

def main(paths):
    files = [Path(p) for p in paths] or [f for d in (".claude/skills", "outils", "docs", "CLAUDE.md")
                                         for f in ([ROOT / d] if (ROOT / d).is_file() else (ROOT / d).rglob("*"))
                                         if f.is_file() and f.suffix in (".md", ".py")]
    refs = {}
    for f in files:
        txt = f.read_text(encoding="utf-8")
        for m in re.finditer(r"LEGIARTI\d{12}", txt):
            contexte = txt[max(0, m.start() - 80):m.end() + 40].lower()
            historique = any(k in contexte for k in ("ancien", "antérieur", "anterieur", "modifi", "futur"))
            refs.setdefault(m.group(), {"fichiers": set(), "historique": False})
            refs[m.group()]["fichiers"].add(str(f.relative_to(ROOT)))
            refs[m.group()]["historique"] |= historique
    p, ko = Piste(), 0
    for ref in sorted(refs):
        try:
            a = p.lf_article(ref)["article"]
            titre = (a.get("textTitles") or [{}])[0].get("titre", "?")
            etat = a.get("etat")
            if etat == "ABROGE_DIFF":
                from piste.sources import ms_to_date
                print(f"[OK ] {ref} art. {a.get('num')} {titre} : en vigueur, abrogation différée au {ms_to_date(a.get('dateFin'))}")
                differes = globals().setdefault("DIFFERES", [])
                differes.append(ref)
                continue
            ok = etat == "VIGUEUR" or (refs[ref]["historique"] and etat in ("MODIFIE", "ABROGE", "VIGUEUR_DIFF"))
            ko += not ok
            note = " (version historique citée comme telle)" if etat != "VIGUEUR" and ok else ""
            print(f"[{'OK ' if ok else 'ATT'}] {ref} art. {a.get('num')} {titre} : {etat}{note}")
        except (PisteError, KeyError, TypeError) as e:
            ko += 1
            print(f"[ERR] {ref} : {e}  ({', '.join(sorted(refs[ref]["fichiers"]))})")
    n_diff = len(globals().get("DIFFERES", []))
    print(f"{len(refs)} références, {ko} problème(s), {n_diff} en abrogation différée")
    sys.exit(1 if ko else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
