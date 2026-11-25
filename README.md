# claude-tv-droit

Outils juridiques pour Claude : sources officielles du droit français (Légifrance, Judilibre via l'API PISTE) exposées en serveur MCP, puis Skills de raisonnement et synthèse de dossiers.

- Roadmap : [docs/00-roadmap.md](docs/00-roadmap.md)
- Accès PISTE : [docs/01-acces-piste.md](docs/01-acces-piste.md)

## Outils MCP (`sources-juridiques`)
| Outil | Rôle |
|---|---|
| `get_article(code, numero, date)` | Texte exact d'un article **dans la version en vigueur à la date donnée** |
| `rechercher_texte(requete, fond, date, nb)` | Codes, lois et décrets, conventions collectives, JO, CNIL |
| `rechercher_jurisprudence(requete, juridiction, date_min, date_max, nb, publiees_seulement)` | Cassation, appel, première instance (Judilibre) ; administratif, constitutionnel (Légifrance) |
| `get_decision(identifiant)` | Texte intégral + métadonnées (ECLI, solution, publication, visas, rapprochements) |
| `calculer_delai(point_de_depart, jours, mois, annees, distance, alsace_moselle)` | Échéance d'un délai de procédure civile (art. 640-643 CPC), reports week-end et fériés |
| `calculer_delai_administratif(recours, point_de_depart, heure, distance, …)` | Recours administratifs et contentieux des étrangers (délais francs, délais en heures) |
| `calculer_delai_penal(procedure, point_de_depart, …)` | Appel, opposition, pourvoi en matière pénale (art. 801 CPP) |
| `calculer_prescription_penale(type_prescription, categorie, date, …)` | Prescription de l'action publique et des peines |

## Skills (`.claude/skills/`)
`recherche-juridique` · `raisonnement-juridique` · `verification-citations` · `droit-dans-le-temps` · `procedure-civile-delais` · `delais-administratifs-etrangers` · `delais-penaux`
Chargés automatiquement par Claude Code dans ce dépôt. Évaluation : `docs/evals/questions.md`.

Chaque résultat porte l'identifiant officiel et l'URL publique ; chaque appel est journalisé dans `logs/audit.jsonl`.

## Installation
```bash
pip install -r requirements.txt
```
Variables d'environnement : `PISTE_ENV` (`prod` | `sandbox`), `PISTE_CLIENT_ID`, `PISTE_CLIENT_SECRET`.

```bash
python3 -m pytest -q tests     # tests hors ligne
python3 -m piste.check         # diagnostic d'accès PISTE
python3 -m outils.verifier_references   # références citées toujours en vigueur ?
python3 -m outils.delais 2026-01-31 --mois 1   # calcul de délai
```

## Utilisation dans Claude Code
Le fichier `.mcp.json` déclare le serveur : lancer `claude` à la racine du dépôt et approuver `sources-juridiques`.
Exemple : « Donne-moi l'article 1240 du Code civil en vigueur au 1er mars 2015 » → Claude doit répondre que c'était alors l'article 1382.
