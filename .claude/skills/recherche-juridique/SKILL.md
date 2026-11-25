---
name: recherche-juridique
description: Méthode de recherche juridique en droit français avec les outils MCP sources-juridiques (Légifrance, Judilibre). À utiliser dès qu'une question demande de trouver ou vérifier un texte de loi, un article de code, une convention collective ou de la jurisprudence (Cour de cassation, cours d'appel, Conseil d'État, Conseil constitutionnel).
---

# Recherche juridique

## Principe
On part des **textes**, puis la **jurisprudence** qui les interprète, puis seulement le raisonnement. Rien n'est cité sans avoir été obtenu par un outil (voir le skill `verification-citations`).

## Protocole
1. **Cadrer** (sans données client dans les requêtes) :
   - matière (civil, social, commercial, administratif, pénal…), juridiction compétente ;
   - **date des faits** : elle détermine la version des textes (skill `droit-dans-le-temps`) ;
   - mots-clés juridiques (qualifications), pas les noms des parties.
2. **Textes** :
   - article connu → `get_article(code, numero, date=<date des faits>)` ;
   - article inconnu → `rechercher_texte(requete, fond="codes", date=…)`, puis `get_article` sur les résultats pertinents ;
   - relation de travail → vérifier aussi `fond="conventions_collectives"` (attention au statut : `ABROGE`, `VIGUEUR`) ;
   - lire le `nota` (entrée en vigueur, application aux instances en cours) et `autres_versions` ;
   - lire le champ `alerte` : `ABROGE_DIFF` = en vigueur mais **abrogation programmée** (ex. tout le CPP au 1er janvier 2029, ordonnance n° 2025-1091) ; `VIGUEUR_DIFF` = version future, pas encore applicable.
3. **Jurisprudence**, de la plus haute à la plus basse :
   - `rechercher_jurisprudence(requete, juridiction="cassation", publiees_seulement=True)` d'abord ;
   - élargir aux non publiées, puis `appel` / `premiere_instance` pour l'état des juges du fond ;
   - ordre administratif : `juridiction="administratif"` ; contrôle de constitutionnalité : `constitutionnel` ;
   - restreindre par dates (`date_min`) pour détecter les **revirements** récents ;
   - ouvrir les décisions retenues avec `get_decision` : lire le **sommaire**, le **visa**, le motif décisif et les **rapprochements**.
4. **Pondérer** la jurisprudence :
   - Assemblée plénière / chambre mixte > arrêt de chambre publié (Bulletin, Rapport) > arrêt non publié ;
   - Conseil d'État : « Publié au recueil Lebon » > « Mentionné aux tables » > « Inédit » ;
   - un arrêt de cour d'appel n'illustre qu'une tendance des juges du fond ;
   - date : un arrêt ancien peut avoir été contredit, chercher plus récent sur la même question.
5. **Restituer** : pour chaque source, identifiant + date + URL + citation exacte du passage utile. Signaler explicitement ce qui n'a **pas** été trouvé.

## Pièges fréquents
- Renumérotations (réforme du droit des obligations au 1er octobre 2016 : l'ancien art. 1382 C. civ. est devenu l'art. 1240) : toujours raisonner avec la version applicable à la date des faits.
- Numérotation des codes : `L1234-1` (sans point ni espace) pour les outils.
- Judilibre ne couvre les cours d'appel et tribunaux que pour les décisions diffusées : absence de résultat ≠ absence de jurisprudence.
- Délais : skills `procedure-civile-delais`, `delais-administratifs-etrangers`, `delais-penaux` (toujours calculer avec les outils).
- HUDOC (CEDH) et CJUE ne sont pas encore branchés : les signaler comme « non vérifié » si on les mentionne.
