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
        for m in re.finditer(r"LEGIARTI\d{12}", f.read_text(encoding="utf-8")):
            refs.setdefault(m.group(), set()).add(str(f.relative_to(ROOT)))
    p, ko = Piste(), 0
    for ref in sorted(refs):
        try:
            a = p.lf_article(ref)["article"]
            titre = (a.get("textTitles") or [{}])[0].get("titre", "?")
            etat = a.get("etat")
            ok = etat == "VIGUEUR"
            ko += not ok
            print(f"[{'OK ' if ok else 'ATT'}] {ref} art. {a.get('num')} {titre} : {etat}")
        except (PisteError, KeyError, TypeError) as e:
            ko += 1
            print(f"[ERR] {ref} : {e}  ({', '.join(sorted(refs[ref]))})")
    print(f"{len(refs)} références, {ko} problème(s)")
    sys.exit(1 if ko else 0)

if __name__ == "__main__":
    main(sys.argv[1:])
