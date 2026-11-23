---
name: droit-dans-le-temps
description: Détermination de la loi applicable dans le temps (version d'un texte à la date des faits, loi nouvelle, dispositions transitoires, prescription et forclusion après une réforme). À utiliser dès qu'un dossier comporte des faits anciens, qu'un texte a été modifié ou renuméroté, ou qu'on calcule une prescription à cheval sur deux lois.
---

# Droit dans le temps

## Textes de base (vérifiés via `get_article`, à re-vérifier en cas de doute)
- Art. 2 C. civ. (LEGIARTI000006419281) : « La loi ne dispose que pour l'avenir ; elle n'a point d'effet rétroactif. »
- Art. 2222 C. civ. (LEGIARTI000019017122, depuis le 2008-06-19) : loi qui **allonge** une prescription ou forclusion → sans effet sur une prescription acquise, s'applique aux délais en cours en tenant compte du temps écoulé ; loi qui **réduit** → le nouveau délai court à compter de l'entrée en vigueur, sans dépasser la durée totale prévue par la loi antérieure.

## Méthode
1. **Dater** chaque fait juridiquement pertinent (conclusion du contrat, fait dommageable, manifestation du dommage, connaissance des faits, saisine du juge).
2. **Version des textes** : `get_article(code, numero, date=<date du fait>)`. Lire `autres_versions` : une modification entre les faits et aujourd'hui doit être signalée.
3. **Nature de la règle** :
   - règle de fond : en principe loi en vigueur au jour du fait générateur ;
   - contrats : en principe loi en vigueur au jour de la conclusion (survie de la loi ancienne), sauf disposition d'ordre public contraire ou texte transitoire ;
   - règle de procédure : en principe application immédiate aux instances en cours, **sous réserve des dispositions transitoires** ;
   - toujours lire le `nota` de l'article, qui reprend souvent les règles d'entrée en vigueur (ex. art. 768 CPC : applicable aux instances en cours au 1er janvier 2020).
4. **Dispositions transitoires** : chercher le texte modificatif (`rechercher_texte(fond="lois_decrets")`), son article d'entrée en vigueur, puis la jurisprudence sur son application dans le temps.
5. **Prescription** : identifier le délai sous la loi ancienne et sous la loi nouvelle, appliquer l'art. 2222, puis vérifier les causes d'interruption/suspension (ex. art. 2241 C. civ., LEGIARTI000019017098 : la demande en justice, même en référé, interrompt la prescription et la forclusion).

## Restitution
Présenter une frise : date du fait → texte applicable (identifiant de version) → éventuelle loi nouvelle → règle transitoire retenue et sa source.
