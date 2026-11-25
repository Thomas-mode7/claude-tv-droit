# Jeu d'évaluation : Skills juridiques + MCP

Pour chaque question : poser la question à Claude dans le dépôt (Skills et MCP actifs), puis cocher les critères.
Critères communs à toutes les questions : ☐ toute référence porte un identifiant + lien ☐ aucune référence non vérifiée sans mention « non vérifié » ☐ aucun nom de partie envoyé dans les outils.

| # | Question | Points attendus (vérifiés sur Légifrance/Judilibre le 2026-11-23) | Skill visé |
|---|---|---|---|
| 1 | Quel texte fonde la responsabilité pour faute, pour des faits de 2012 ? | Art. 1382 C. civ. (version applicable en 2012), et non 1240 ; mention de la renumérotation au 2016-10-01 | droit-dans-le-temps |
| 2 | Que disait l'art. 1240 C. civ. au 1er janvier 2010 ? | Texte sur le paiement de bonne foi (LEGIARTI000006437044), version modifiée au 2016-10-01 | droit-dans-le-temps |
| 3 | Jugement contentieux notifié le 31/01/2026 : jusqu'à quand faire appel ? | 1 mois (art. 538) → 28/02/2026 samedi → **lundi 02/03/2026** à 24h | procedure-civile-delais |
| 4 | Même question, l'appelant demeure au Canada. | +2 mois (art. 643) → échéance théorique 30/04/2026 (jeudi) ; vérifier que le calcul est fait avec l'outil | procedure-civile-delais |
| 5 | Décision notifiée le 14/04/2026, délai d'un mois. | 14/05/2026 = Ascension → **vendredi 15/05/2026** | procedure-civile-delais |
| 6 | Délai de pourvoi en cassation de droit commun ? | 2 mois, sauf disposition contraire (art. 612 CPC, LEGIARTI000006410964) | procedure-civile-delais |
| 7 | Délai de prescription d'une action en paiement d'une facture entre particuliers, point de départ ? | 5 ans, connaissance des faits (art. 2224 C. civ.) ; signaler les délais spéciaux possibles (ex. consommation) comme à vérifier | procedure-civile-delais |
| 8 | Une loi réduit un délai de prescription : comment s'applique-t-elle aux délais en cours ? | Art. 2222 al. 2 C. civ. : nouveau délai à compter de l'entrée en vigueur, durée totale plafonnée à l'ancienne | droit-dans-le-temps |
| 9 | Une assignation en référé interrompt-elle la prescription ? | Oui, art. 2241 C. civ. (même en référé, même devant une juridiction incompétente) | recherche-juridique |
| 10 | Que doivent contenir des conclusions devant le tribunal judiciaire ? | Art. 768 CPC : prétentions, moyens, pièces numérotées, bordereau, structure faits/discussion/dispositif, récapitulation ; nota : applicable aux instances en cours au 01/01/2020 | recherche-juridique |
| 11 | Trouve un arrêt publié de la Cour de cassation sur l'indemnisation en cas de faute inexcusable de l'employeur. | Ex. Cass. 2e civ., 22 janv. 2015, n° 14-10.584, Bulletin (ECLI:FR:CCASS:2015:C200088), visa art. L. 452-1 CSS ; recherche avec `publiees_seulement` | recherche-juridique |
| 12 | Vérifie cette phrase : « Selon l'article 1382 du Code civil, en vigueur aujourd'hui, tout fait quelconque… » | Erreur relevée : depuis le 2016-10-01, c'est l'art. 1240 ; tableau de vérification | verification-citations |
| 13 | Un client te décrit un litige (vente d'un véhicule d'occasion en panne 2 mois après) : analyse. | Structure faits → qualifications concurrentes (vice caché / conformité / dol) → problème de droit → règles vérifiées → application → arguments adverses → délais ; questions au client | raisonnement-juridique |
| 14 | Rédige une consultation sur la question 13. | Suit `trame-consultation.md` ; sources vérifiées en annexe ; mention de validation par l'avocat | raisonnement-juridique |
| 15 | Arrêté préfectoral notifié le 3 janvier 2026 : jusqu'à quand saisir le tribunal administratif ? | Délai franc de 2 mois → **mercredi 4 mars 2026** ; CE avis 9 juin 2026 n° 512314 ; R421-5 (mention des voies de recours) | delais-administratifs-etrangers |
| 16 | Étranger assigné à résidence, OQTF notifiée le vendredi 18 avril 2025 : dernier jour du recours ? | 7 jours francs (L921-1) → samedi 26 → **lundi 28 avril 2025** (CE 10 août 2026 n° 508820) | delais-administratifs-etrangers |
| 17 | Étranger en rétention, OQTF notifiée le vendredi 27/11/2026 à 17h45 : délai ? | 48 h d'heure à heure (L921-2, R921-2-1) → **dimanche 29/11/2026 à 17h45**, pas de report | delais-administratifs-etrangers |
| 18 | Arrêt correctionnel prononcé le 17/12/2026 : délai de pourvoi ? | 10 jours francs (art. 568 depuis le 30/09/2024) → 27/12 dimanche → **lundi 28/12/2026** ; échéance prudente | delais-penaux |
| 19 | Délit commis le 10/01/2015, aucun acte : est-il prescrit aujourd'hui ? | Ancien délai de 3 ans non acquis au 01/03/2017 → loi nouvelle, 6 ans (112-2 4°) → prescrit le **10/01/2021** | delais-penaux |
| 20 | Les règles de prescription pénale seront-elles les mêmes en 2029 ? | Signale la réécriture du CPP par l'ordonnance n° 2025-1091 au 01/01/2029 (articles en abrogation différée) | delais-penaux, recherche-juridique |

Résultats : noter dans `docs/evals/resultats-AAAA-MM-JJ.md` (question, critères OK/KO, remarque).
