---
name: verification-citations
description: Contrôle anti-hallucination des références juridiques. À appliquer avant de livrer toute réponse, note, consultation ou conclusions qui cite un article de loi, une décision de justice ou une convention collective, et quand l'utilisateur demande de vérifier des citations dans un document.
---

# Vérification des citations

## Règle d'or
**Une référence n'existe dans la réponse que si un outil `sources-juridiques` l'a renvoyée pendant la session.** Sinon elle est marquée « non vérifié », ou supprimée.

## Procédure (avant de livrer)
1. **Lister** toutes les références de la réponse : articles (code + numéro), décisions (juridiction, date, n° de pourvoi/RG, ECLI), textes (loi, décret, convention).
2. **Rapprocher** chaque référence d'un appel d'outil :
   - article → `get_article` avec la bonne date ; le texte cité doit être **mot pour mot** celui renvoyé ;
   - décision → `get_decision` ; vérifier juridiction, chambre, date, numéro, solution ; une citation entre guillemets doit figurer dans `texte` ;
   - convention collective → `rechercher_texte(fond="conventions_collectives")`, vérifier le statut.
3. **Contrôler la portée** : la décision dit-elle vraiment ce qu'on lui fait dire ? (attendu de principe ou simple motif d'espèce, rejet ou cassation, publiée ou non).
4. **Contrôler la version** : article en vigueur à la date des faits ? (`en_vigueur_du` / `en_vigueur_jusqu_au`).
5. **Corriger** : remplacer par la référence vérifiée, ou retirer, ou marquer « non vérifié ».

## Format de citation
- Article : *art. 1240 C. civ. (LEGIARTI000032041571, version en vigueur depuis le 2016-10-01)* + lien.
- Cassation : *Cass. 2e civ., 22 janv. 2015, n° 14-10.584, publié au Bulletin (ECLI:FR:CCASS:2015:C200088)* + lien.
- Conseil d'État : *CE, [formation], [date], n° [requête], [Lebon / tables / inédit]* + lien.

## Vérifier un document fourni par l'utilisateur
Produire un tableau : référence telle qu'écrite | résultat (conforme / erreur de numéro / version non applicable / citation inexacte / introuvable) | référence corrigée | lien.
Le journal `logs/audit.jsonl` trace les appels effectués.
