# Roadmap : Claude + outils juridiques

Légende : 🤖 fait/automatisable par Claude · 👤 action de votre part · ✅ livré

## Phase 0 : Accès PISTE (jour 1)
- ✅🤖 Client OAuth2 Légifrance + Judilibre, cache de token, retries, tests (`piste/`)
- ✅🤖 Diagnostic `piste/check.py`, `.env.example`, `.gitignore`
- ✅👤 Création compte/application PISTE (production) + souscription Légifrance et Judilibre
- ✅🤖 Diagnostic tout vert en production
- **Sortie** : ✅ `python -m piste.check` tout vert

## Phase 1 : Serveur MCP « sources » (semaine 1)
- ✅🤖 Outils : `get_article(code, num, date)`, `rechercher_texte`, `rechercher_jurisprudence`, `get_decision(id)`
- ✅🤖 Sortie normalisée : texte verbatim + identifiant (LEGIARTI/ECLI) + date de version + URL
- ✅🤖 Journal d'audit de chaque appel (`logs/audit.jsonl`)
- ✅🤖 Branchement Claude Code (`.mcp.json`) ; 🤖 connecteur claude.ai (serveur HTTP hébergé) si besoin
- ✅🤖 Jurisprudence déjà couverte : Cassation, cours d'appel, 1re instance (Judilibre), Conseil d'État/CAA/TA, Conseil constitutionnel
- **Sortie** : ✅ l'art. 1240 C. civ. demandé au 01/01/2010 renvoie bien l'ancien texte (paiement) ; la responsabilité était alors à l'art. 1382

## Phase 2 : Jurisprudence élargie (semaines 2-3)
- ✅🤖 Judilibre (cc, ca, tj, tcom, cph), JADE (Conseil d'État, CAA, TA), CONSTIT : livrés en phase 1
- 🤖 HUDOC (CEDH) : adaptateur isolé, signalé « non officiel », avec tests de non-régression
- 🤖 Option : CJUE via EUR-Lex/CELLAR
- 🤖 Métadonnées de poids : formation, publication au Bulletin, solution, décisions liées
- **Sortie** : recherche multi-juridictions avec un format unifié

## Phase 3 : Skills de raisonnement (semaines 2-4, en parallèle)
- 🤖 Brouillons : `recherche-juridique`, `raisonnement-juridique`, `verification-citations`, `droit-dans-le-temps`, `procedure-civile` (délais CPC)
- 👤 Relecture par un juriste, ajout de vos trames maison (1 Skill par matière : civil, social, admin…)
- 🤖 Jeu de tests : 20 questions types avec réponses de référence, pour mesurer avant/après
- **Sortie** : plus aucune citation sans appel d'outil correspondant

## Phase 4 : Synthèse de dossiers (semaines 4-6)
- 🤖 Pipeline : OCR/ingestion → classement des pièces → extraction JSON par document → fiche de synthèse sourcée
- 🤖 Skill `synthese-dossier` (parties, chronologie, prétentions, moyens, pièces par moyen, points litigieux, échéances)
- 🤖 Sous-agents par bloc de pièces pour les gros dossiers
- 👤 2-3 dossiers anonymisés comme jeu d'essai
- **Sortie** : fiche de synthèse avec renvois pièce/page

## Phase 5 : Sécurité et déploiement (en continu, bloquant avant données réelles)
- 👤 Choix du déploiement (DPA, rétention, hébergement), validation déontologique (secret professionnel)
- 🤖 Anonymisation à l'entrée, secrets hors dépôt, droits minimaux, journalisation
- 👤 Passage en production PISTE, formation des utilisateurs, procédure « l'avocat valide »

## Jalons
| Jalon | Critère de réussite |
|---|---|
| J1 | Diagnostic PISTE vert |
| S1 | MCP sources utilisable dans Claude |
| S3 | Jurisprudence multi-sources + premiers Skills |
| S6 | Synthèse de dossier sur cas réels anonymisés |
