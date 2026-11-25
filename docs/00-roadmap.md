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

## Phase 3 : Skills de raisonnement
- ✅🤖 Skills (`.claude/skills/`) : `recherche-juridique`, `raisonnement-juridique` (+ trame de consultation), `verification-citations`, `droit-dans-le-temps`, `procedure-civile-delais`
- ✅🤖 Calculateur de délais déterministe (art. 640-643 CPC, fériés, Alsace-Moselle) : `outils/delais.py` + outil MCP `calculer_delai`
- ✅🤖 Contrôle automatique des références citées dans le dépôt : `python3 -m outils.verifier_references` (59 références : toutes valides, 19 en abrogation différée au 01/01/2029)
- ✅🤖 Délais administratifs et contentieux des étrangers (CJA, CESEDA réformé en juin 2026, délais francs selon CE avis n° 512314, délais en heures) : `outils/delais_admin.py` + outil MCP `calculer_delai_administratif` + Skill `delais-administratifs-etrangers`
- ✅🤖 Délais de procédure pénale et prescription (action publique, peine, réforme 2017, infractions occultes, interruption, alerte recodification du CPP au 01/01/2029) : `outils/delais_penal.py` + outils MCP `calculer_delai_penal`, `calculer_prescription_penale` + Skill `delais-penaux`
- ✅🤖 Jeu d'évaluation de 20 questions : `docs/evals/questions.md`
- 👤 Relecture des Skills par un juriste ; ajout de vos trames maison et d'un Skill par matière (civil, social, admin…)
- 🤖 Passer le jeu d'évaluation et consigner les résultats
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
