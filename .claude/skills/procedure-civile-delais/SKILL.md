---
name: procedure-civile-delais
description: Calcul et contrôle des délais de procédure civile (appel, pourvoi, opposition, comparution, délais en jours ou en mois, report au jour ouvrable, augmentation pour distance) et des délais de prescription. À utiliser dès qu'il faut dire jusqu'à quand un acte peut être accompli ou si un recours est encore recevable.
---

# Délais de procédure civile

Pour l'administratif et les étrangers : skill `delais-administratifs-etrangers` ; pour le pénal : skill `delais-penaux`.

## Toujours calculer avec l'outil, jamais de tête
- MCP : `calculer_delai(point_de_depart, jours|mois|annees, distance, alsace_moselle)`
- ou en ligne de commande : `python3 -m outils.delais 2026-01-31 --mois 1`

## Règles appliquées par l'outil (vérifiées sur Légifrance)
| Article CPC | Identifiant | Règle |
|---|---|---|
| 640 | LEGIARTI000006411001 | Origine : date de l'acte, de l'événement, de la décision ou de la notification |
| 641 | LEGIARTI000006411002 | En jours : le jour de départ ne compte pas. En mois/années : même quantième, à défaut dernier jour du mois. Mois puis jours |
| 642 | LEGIARTI000006411003 | Expire à 24h ; samedi, dimanche, férié ou chômé → premier jour ouvrable suivant |
| 643 | LEGIARTI000034747123 | +1 mois (outre-mer), +2 mois (étranger) pour comparution, appel, opposition, tierce opposition (586 al. 3), révision, pourvoi |

Fériés : C. trav. L3133-1 (LEGIARTI000033020901) ; Alsace-Moselle L3134-13 (LEGIARTI000006902635 : Vendredi saint dans les communes ayant un temple protestant ou une église mixte, 26 décembre).

## Délais de droit commun (à confirmer par `get_article` à la date utile)
- Recours ordinaire (appel, opposition) : **1 mois** en matière contentieuse, **15 jours** en matière gracieuse (art. 538 CPC, LEGIARTI000006410858).
- Pourvoi en cassation : **2 mois**, sauf disposition contraire (art. 612 CPC, LEGIARTI000006410964).
- Point de départ des recours : notification du jugement, sauf texte contraire ; le délai court aussi contre celui qui notifie (art. 528 CPC, LEGIARTI000006410842).
- Prescription de droit commun des actions personnelles ou mobilières : **5 ans** à compter du jour où le titulaire a connu ou aurait dû connaître les faits (art. 2224 C. civ., LEGIARTI000019017112).

## Méthode
1. Identifier **l'acte à accomplir** et **le texte qui fixe son délai**. Les délais spéciaux sont nombreux (référé, procédure à jour fixe, matière prud'homale, procédure collective, baux…) : chercher le texte spécial avant d'appliquer le droit commun.
2. Identifier le **point de départ** et vérifier sa régularité (notification régulière ? mentions des voies de recours ?).
3. Lancer `calculer_delai`, avec `distance` si la partie demeure outre-mer ou à l'étranger.
4. Restituer : échéance, jour de la semaine, reports appliqués, textes, **avertissements** de l'outil.
5. Conseil de prudence : recommander d'agir avant l'échéance calculée ; signaler toute incertitude sur le point de départ.
