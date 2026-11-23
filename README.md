# claude-tv-droit

Outils juridiques pour Claude : accès Légifrance et Judilibre (API PISTE), puis serveur MCP, Skills de raisonnement et synthèse de dossiers.

- Roadmap : [docs/00-roadmap.md](docs/00-roadmap.md)
- Accès PISTE : [docs/01-acces-piste.md](docs/01-acces-piste.md)

## Démarrage
Variables d'environnement requises (dans l'environnement cloud, ou un fichier `.env` local jamais commité) :
`PISTE_ENV` (`sandbox` | `prod`), `PISTE_CLIENT_ID`, `PISTE_CLIENT_SECRET`.

```bash
python3 -m pytest -q tests     # tests unitaires (sans réseau)
python3 -m piste.check         # diagnostic d'accès PISTE
```
