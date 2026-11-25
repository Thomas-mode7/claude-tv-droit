---
name: delais-penaux
description: Calcul et contrôle des délais de procédure pénale (appel correctionnel, de police, d'assises, du procureur général, appel incident, appel des ordonnances du juge d'instruction, opposition, pourvoi) et de la prescription pénale (action publique, peine, réforme de 2017, infractions occultes, interruption). À utiliser dès qu'une question porte sur la recevabilité d'un recours pénal ou sur la prescription d'une infraction ou d'une peine.
---

# Délais pénaux et prescription

## Toujours calculer avec l'outil
- Procédure : MCP `calculer_delai_penal(procedure, point_de_depart, reside_hors_metropole)`.
- Prescription : MCP `calculer_prescription_penale(type_prescription, categorie, date, dernier_acte_interruptif, date_apparition, ...)`.

## Alerte : recodification au 1er janvier 2029
Le code de procédure pénale (partie législative) est réécrit par l'**ordonnance n° 2025-1091 du 19 novembre 2025** à compter du **1er janvier 2029**. Tous les articles du CPP cités ci-dessous, et plusieurs articles du code pénal (dont 133-2 à 133-4), sont en **abrogation différée** à cette date (état `ABROGE_DIFF` dans `get_article`). Exemple : à compter de 2029, l'art. 133-2 C. pén. renvoie aux art. L. 5111-4 à L. 5111-10 du nouveau CPP (version future LEGIARTI000052851466).
- Pour un acte ou une échéance avant le 1er janvier 2029 : les articles ci-dessous s'appliquent.
- À partir de 2029 : appeler `get_article(..., date=<date utile>)` et chercher les nouveaux articles ; vérifier les dispositions transitoires de l'ordonnance.
- Les outils de calcul ajoutent automatiquement un avertissement quand l'échéance tombe en 2029 ou après.

## Délais de procédure (vérifiés)
Règle générale : tout délai de procédure pénale expire le dernier jour à 24h ; samedi, dimanche, férié ou chômé → premier jour ouvrable suivant (CPP 801, LEGIARTI000006578399).

| Acte | `procedure` | Délai | Point de départ | Source |
|---|---|---|---|---|
| Appel jugement correctionnel / de police | `appel_correctionnel` | 10 jours | prononcé (signification dans les cas de l'al. 2) | CPP 498 (LEGIARTI000021331547), 547 |
| Appel incident | `appel_incident` | +5 jours | appel principal | CPP 500 (LEGIARTI000006576759) |
| Appel du procureur général (condamnation) | `appel_procureur_general` | 20 jours | prononcé | CPP 505 (LEGIARTI000021331544) |
| Appel arrêt de cour d'assises | `appel_assises` | 10 jours | prononcé | CPP 380-9 (LEGIARTI000044568457) |
| Appel ordonnance du juge d'instruction | `appel_ordonnance_instruction` | 10 jours | notification ou signification | CPP 186 (LEGIARTI000048441733) |
| Opposition (signification à personne) | `opposition` | 10 jours / 1 mois hors métropole | signification | CPP 491 (LEGIARTI000006576719) |
| Pourvoi en cassation | `pourvoi` | **10 jours francs** (décisions depuis le 30/09/2024), 5 jours francs avant | lendemain du prononcé | CPP 568 (LEGIARTI000048442131) |

Vigilance : la déclaration se fait au greffe, aux heures d'ouverture ; un pourvoi tardif est irrecevable sauf force majeure (Cass. crim., 13 janv. 2015, n° 13-87.188, Bull., ECLI:FR:CCASS:2015:CR07484). Pour le pourvoi, l'outil retient l'échéance prudente.

## Prescription de l'action publique (vérifiée)
- Droit commun depuis le 1er mars 2017 : crimes 20 ans (CPP 7, LEGIARTI000043409351), délits 6 ans (CPP 8, LEGIARTI000049531911), contraventions 1 an (CPP 9, LEGIARTI000034099775), « à compter du jour où l'infraction a été commise ».
- Avant le 1er mars 2017 : 10 ans / 3 ans / 1 an (versions antérieures des art. 7, 8, 9). Les lois de prescription s'appliquent immédiatement si la prescription n'est pas acquise (C. pén. 112-2 4°, LEGIARTI000006417182) : l'outil vérifie si l'ancienne prescription était acquise au 1er mars 2017.
- Infraction occulte ou dissimulée : point de départ au jour où elle est apparue et a pu être constatée, avec un butoir de 12 ans (délits) ou 30 ans (crimes) à compter de la commission (CPP 9-1, LEGIARTI000037289466).
- Interruption : nouveau délai de même durée à compter de l'acte (CPP 9-2, LEGIARTI000043409311) ; suspension : obstacle de droit ou de fait insurmontable (CPP 9-3, LEGIARTI000034098595) : **non calculée**, à ajouter.
- **Régimes spéciaux non automatisés** (mineurs victimes avec point de départ à la majorité et délais de 30/20/10 ans, crimes de l'art. 7 al. 2, presse, fiscal…) : vérifier le texte avec `get_article`, puis passer `duree_speciale_annees` et `point_de_depart_special`.

## Prescription des peines (vérifiée)
20 ans (crimes, C. pén. 133-2, LEGIARTI000034099845), 6 ans (délits, 133-3, LEGIARTI000034099836), 3 ans (contraventions, 133-4, LEGIARTI000006417513), à compter de la date à laquelle la condamnation est devenue définitive ; régimes spéciaux aux alinéas 2 et 3 des art. 133-2 et 133-3.

## Méthode
1. Qualifier l'infraction (crime, délit, contravention) et repérer tout régime spécial.
2. Dater : commission, apparition (si occulte), actes interruptifs (liste précise de l'art. 9-2), éventuelles suspensions.
3. Lancer l'outil ; lire les `etapes` et `avertissements`.
4. Restituer : échéance, régime appliqué (loi ancienne / nouvelle), actes pris en compte, points non calculés.
