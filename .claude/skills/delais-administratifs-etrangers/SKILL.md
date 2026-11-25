---
name: delais-administratifs-etrangers
description: Calcul et contrôle des délais de recours en contentieux administratif (recours pour excès de pouvoir, plein contentieux, décision implicite, appel, cassation, distance) et en contentieux des étrangers (OQTF, assignation à résidence, rétention, transfert Dublin, refus d'entrée, CNDA, juge des libertés). À utiliser dès qu'il faut dire jusqu'à quand un recours administratif ou un recours d'étranger est recevable.
---

# Délais administratifs et contentieux des étrangers

## Toujours calculer avec l'outil
MCP `calculer_delai_administratif(recours, point_de_depart, heure, distance, alsace_moselle, decision_implicite)`.
Jamais de calcul de tête : les règles (délai franc, heures, report) changent l'échéance d'un à deux jours.

## Règles générales (vérifiées)
- **Délai de droit commun** : 2 mois à compter de la notification ou publication (CJA R421-1, LEGIARTI000039807005) ; décision implicite de rejet : 2 mois à compter de sa naissance (R421-2, LEGIARTI000039807000) ; silence de 2 mois = acceptation par principe (CRPA L231-1, LEGIARTI000031367611), rejet dans les cas de L231-4 (LEGIARTI000031367619).
- **Délais francs** : « sauf texte contraire, les délais de recours devant les juridictions administratives sont, en principe, des délais francs, leur premier jour étant le lendemain du jour de leur déclenchement et leur dernier jour étant le lendemain du jour de leur échéance (...). Lorsque ce délai expire un samedi, un dimanche ou un jour férié, un recours reste recevable le premier jour ouvrable suivant. » CE, avis, 9 juin 2026, n° 512314, Lebon (ECLI:FR:CECHR:2026:512314.20260609).
- **Opposabilité** : délais opposables seulement s'ils sont mentionnés, avec les voies de recours, dans la notification (R421-5, LEGIARTI000006449946). Toujours vérifier la notification.
- **Distance** : +1 mois outre-mer, +2 mois étranger, pour le recours de R421-1 (R421-7, LEGIARTI000031180453).
- Appel : 2 mois (R811-2, LEGIARTI000026829556) ; cassation : 2 mois (R821-1, LEGIARTI000006450393), sauf texte contraire.

## Contentieux des étrangers (CESEDA, réformé : loi n° 2024-42 puis décrets n° 2026-455 et 2026-456 au 8 juin 2026)
| Situation | `recours` | Délai | Nature | Sources |
|---|---|---|---|---|
| OQTF avec délai de départ, décisions accompagnant (L614-1) | `etrangers_un_mois` | 1 mois | franc ; pas de prorogation par recours administratif | L911-1, R911-1 (LEGIARTI000054213317) |
| Étranger assigné à résidence (L614-2), détenu (L614-3), transfert Dublin (L572-4), assignation (L732-8) | `etrangers_sept_jours` | 7 jours | **franc + report** (CE, avis n° 512314) | L921-1 (LEGIARTI000049050149) |
| Étranger en rétention, refus d'entrée au titre de l'asile (L352-4) | `etrangers_48_heures` | 48 h | **heure à heure, sans report** | L921-2, R921-2-1 al. 1 (LEGIARTI000054213234), R921-3 |
| Rétention, plus de droit de rester (art. 68 §3 règl. 2024/1348) | `retention_cinq_jours` | 5 jours | non tranché → échéance prudente | R921-2-1 al. 2 |
| Transfert Dublin d'un étranger en rétention | `dublin_retention_sept_jours` | 7 jours | non tranché → échéance prudente | R921-2-1 al. 3 |
| Recours CNDA contre une décision OFPRA | `cnda` | 1 mois | à vérifier → échéance prudente | R532-10 (LEGIARTI000054215126) |
| Contestation du placement en rétention (juge judiciaire) | `jld_retention_96_heures` | 96 h | heure à heure | L741-10 (LEGIARTI000052086430) |

Points de vigilance :
- **Heure de notification** indispensable pour les délais en heures (décompte d'heure à heure : CAA Marseille, 7 avr. 2022, 21MA04263 ; CAA Lyon, 9 janv. 2020, 19LY00133).
- Les délais de L921-1 et R921-2-1 « ne sont susceptibles d'aucune prorogation » (R921-3, LEGIARTI000054214383) : pas de prorogation par recours administratif ou demande d'aide juridictionnelle. Cela n'a pas empêché le Conseil d'État de juger le délai de 7 jours franc et reporté au jour ouvrable.
- **Changement de situation** en cours de délai (assignation, rétention, détention) : le délai initial est interrompu et un nouveau délai court à compter de l'information (R921-1, R921-2) : recalculer à partir de cette date.
- **Décisions notifiées avant le 8 juin 2026** : vérifier la version applicable avec `get_article(..., date=<date de la décision>)`.
- Pour toute échéance marquée « prudente » : conseiller de déposer avant cette date ; mentionner l'échéance en lecture franche comme simple information.

## Restitution
Échéance (date et, le cas échéant, heure), jour de la semaine, nature du délai (franc ou non), reports appliqués, sources, avertissements de l'outil, et vérifications restant à faire (régularité de la notification, mentions des voies de recours).
