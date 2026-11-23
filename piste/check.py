"""Diagnostic d'accès PISTE : `python3 -I -m piste.check` (depuis la racine du projet)."""
import sys
from .client import Piste, PisteError

def step(name, fn):
    try:
        out = fn(); print(f"[OK ] {name}: {str(out)[:120]}"); return True
    except PisteError as e:
        print(f"[ERR] {name}: {e}"); return False

def main():
    p = Piste(); print(f"Environnement: {p.env}")
    ok = step("OAuth token", lambda: p.token()[:12] + "…")
    if not ok: sys.exit(1)
    a = step("Légifrance ping", p.lf_ping)
    b = step("Légifrance art. 1240 Code civil", lambda: p.lf_search_code_article("Code civil", "1240"))
    c = step("Judilibre healthcheck", p.jl_health)
    c2 = step("Judilibre recherche 'responsabilité'", lambda: p.jl_search("responsabilité", page_size=1))
    sys.exit(0 if all([a, b, c, c2]) else 2)

if __name__ == "__main__":
    main()
