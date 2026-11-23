"""Client PISTE minimal (OAuth2 client_credentials) pour Légifrance et Judilibre.

Aucune dépendance hors `requests`. Le token est mis en cache (expire ~1h).
"""
from __future__ import annotations
import json, os, time
from pathlib import Path
import requests

HOSTS = {
    "sandbox": {
        "oauth": "https://sandbox-oauth.piste.gouv.fr/api/oauth/token",
        "legifrance": "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app",
        "judilibre": "https://sandbox-api.piste.gouv.fr/cassation/judilibre/v1.0",
    },
    "prod": {
        "oauth": "https://oauth.piste.gouv.fr/api/oauth/token",
        "legifrance": "https://api.piste.gouv.fr/dila/legifrance/lf-engine-app",
        "judilibre": "https://api.piste.gouv.fr/cassation/judilibre/v1.0",
    },
}
CACHE = Path(__file__).resolve().parent.parent / ".token_cache.json"


def load_env(path: Path | None = None) -> None:
    """Charge .env sans dépendance (n'écrase pas les variables déjà définies)."""
    path = path or Path(__file__).resolve().parent.parent / ".env"
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.split("#", 1)[0].strip()
            if "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


class PisteError(RuntimeError):
    pass


class Piste:
    def __init__(self, env: str | None = None, client_id: str | None = None,
                 client_secret: str | None = None, timeout: int = 30):
        load_env()
        self.env = env or os.environ.get("PISTE_ENV", "sandbox")
        if self.env not in HOSTS:
            raise PisteError(f"PISTE_ENV invalide: {self.env!r} (sandbox|prod)")
        self.h = HOSTS[self.env]
        self.cid = client_id or os.environ.get("PISTE_CLIENT_ID", "")
        self.secret = client_secret or os.environ.get("PISTE_CLIENT_SECRET", "")
        self.timeout = timeout
        self.s = requests.Session()

    # -- auth ---------------------------------------------------------------
    def token(self) -> str:
        if not self.cid or not self.secret:
            raise PisteError("PISTE_CLIENT_ID / PISTE_CLIENT_SECRET manquants (voir docs/01-acces-piste.md)")
        try:
            c = json.loads(CACHE.read_text())
            if c.get("env") == self.env and c.get("cid") == self.cid and c["exp"] > time.time() + 60:
                return c["token"]
        except Exception:
            pass
        r = self.s.post(self.h["oauth"], timeout=self.timeout, data={
            "grant_type": "client_credentials", "client_id": self.cid,
            "client_secret": self.secret, "scope": "openid"})
        if r.status_code != 200:
            raise PisteError(f"OAuth {r.status_code}: {r.text[:200]}")
        j = r.json()
        CACHE.write_text(json.dumps({"env": self.env, "cid": self.cid, "token": j["access_token"],
                                     "exp": time.time() + int(j.get("expires_in", 3600))}))
        CACHE.chmod(0o600)
        return j["access_token"]

    # -- http ---------------------------------------------------------------
    def call(self, api: str, method: str, path: str, **kw):
        for attempt in range(3):
            r = self.s.request(method, self.h[api] + path, timeout=self.timeout,
                               headers={"Authorization": f"Bearer {self.token()}", "accept": "application/json"}, **kw)
            if r.status_code == 401 and attempt == 0:
                CACHE.unlink(missing_ok=True); continue
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(2 ** attempt); continue
            break
        if r.status_code >= 400:
            raise PisteError(f"{api} {method} {path} -> {r.status_code}: {r.text[:300]}")
        return r.json() if r.content else None

    # -- Légifrance ---------------------------------------------------------
    def lf_ping(self):
        return self.s.get(self.h["legifrance"] + "/list/ping", timeout=self.timeout,
                          headers={"Authorization": f"Bearer {self.token()}"}).text

    def lf_article(self, article_id: str):
        """article_id = LEGIARTI000..."""
        return self.call("legifrance", "POST", "/consult/getArticle", json={"id": article_id})

    def lf_search_code_article(self, code_name: str, num: str, date_ms: int | None = None):
        """Recherche d'un article par numéro dans un code (ex. 'Code civil', '1240')."""
        body = {"recherche": {"champs": [{"typeChamp": "NUM_ARTICLE", "criteres": [
                    {"typeRecherche": "EXACTE", "valeur": num, "operateur": "ET"}], "operateur": "ET"}],
                "pageNumber": 1, "pageSize": 5, "operateur": "ET", "sort": "PERTINENCE", "typePagination": "ARTICLE"},
                "fond": "CODE_DATE"}
        if date_ms:
            body["recherche"]["filtres"] = [{"facette": "DATE_VERSION", "singleDate": date_ms}]
        body["recherche"]["filtres"] = body["recherche"].get("filtres", []) + [
            {"facette": "NOM_CODE", "valeurs": [code_name]}]
        return self.call("legifrance", "POST", "/search", json=body)

    # -- Judilibre ----------------------------------------------------------
    def jl_health(self):
        return self.call("judilibre", "GET", "/healthcheck")

    def jl_search(self, query: str, **filters):
        return self.call("judilibre", "GET", "/search", params={"query": query, **filters})

    def jl_decision(self, decision_id: str):
        return self.call("judilibre", "GET", "/decision", params={"id": decision_id})
