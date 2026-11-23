import json, time
from unittest import mock
import piste.client as C

class R:
    def __init__(s, code=200, j=None, text=""): s.status_code, s._j, s.text = code, j, text; s.content = b"x"
    def json(s): return s._j

def test_token_and_cache(tmp_path):
    C.CACHE = tmp_path / "t.json"
    p = C.Piste(env="sandbox", client_id="id", client_secret="sec")
    with mock.patch.object(p.s, "post", return_value=R(j={"access_token": "abc", "expires_in": 3600})) as post:
        assert p.token() == "abc"; assert p.token() == "abc"
        assert post.call_count == 1  # second call served from cache

def test_missing_creds(monkeypatch):
    for k in ("PISTE_CLIENT_ID", "PISTE_CLIENT_SECRET"): monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr(C, "load_env", lambda *a: None)
    p = C.Piste(env="sandbox", client_id="", client_secret="")
    try: p.token(); assert False
    except C.PisteError as e: assert "manquants" in str(e)

def test_401_refreshes_token(tmp_path):
    C.CACHE = tmp_path / "t.json"
    p = C.Piste(env="prod", client_id="id", client_secret="sec")
    with mock.patch.object(p.s, "post", return_value=R(j={"access_token": "t", "expires_in": 3600})), \
         mock.patch.object(p.s, "request", side_effect=[R(401), R(j={"ok": 1})]) as req:
        assert p.jl_health() == {"ok": 1}; assert req.call_count == 2
