# claude-tv-droit : consignes pour Claude

Projet : outils juridiques (droit français) pour Claude. Voir `docs/00-roadmap.md`.

## Règles de travail juridique (impératives)
- Ne jamais citer un article de loi ou une décision de mémoire : l'obtenir d'abord via le serveur MCP `sources-juridiques`.
- Toujours donner l'identifiant officiel (LEGIARTI…, ECLI, n° de pourvoi / RG) et l'URL renvoyés par l'outil.
- Pour un article : appeler `get_article` avec la **date des faits** ; signaler s'il existe d'autres versions.
- Une source non vérifiée doit être marquée « non vérifié ».
- Délais : toujours `calculer_delai` (ou `python3 -m outils.delais`), jamais de calcul de tête.
- Skills juridiques dans `.claude/skills/` ; après modification d'un Skill citant des LEGIARTI, lancer `python3 -m outils.verifier_references`.
- Ne jamais envoyer d'éléments de dossiers clients (noms, faits identifiants) dans les requêtes de recherche.

## Technique
- Identifiants PISTE : variables d'environnement `PISTE_ENV`, `PISTE_CLIENT_ID`, `PISTE_CLIENT_SECRET` (jamais dans le dépôt).
- Dépendances : `pip install -r requirements.txt`
- Tests hors ligne : `python3 -m pytest -q tests` ; diagnostic réseau : `python3 -m piste.check`
- Code : `piste/client.py` (HTTP/OAuth), `piste/sources.py` (normalisation, audit), `mcp_server.py` (outils MCP).
- Journal d'audit des appels : `logs/audit.jsonl` (non versionné).
- SDK MCP v2 : `from mcp.server.mcpserver import MCPServer` (FastMCP n'existe plus en v2).
