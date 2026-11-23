# Accès PISTE : ce que vous seul pouvez faire (≈15 min)

Je ne peux pas créer le compte à votre place (identité, CGU, éventuelle validation). Tout le reste est automatisé.

1. **Compte** : https://piste.gouv.fr → « Créer un compte » (courriel + validation).
2. **Sandbox d'abord** : en haut, choisir l'environnement *Sandbox* (accès immédiat, données de test).
3. **Créer une application** : *Mes applications* → *Nouvelle application*. Nom libre (ex. `claude-juridique`).
4. **Souscrire aux API** (onglet « API » de l'application) :
   - **Légifrance** (DILA) : accepter les CGU
   - **Judilibre** (Cour de cassation) : accepter les CGU
   - optionnel : API Conseil d'État / JADE si listée séparément
5. **Récupérer** `client_id` et `client_secret` (onglet « Informations d'identification », OAuth).
6. **Production** : refaire 3-5 en *Production*. Certaines API demandent un délai de validation ; la sandbox suffit pour développer.
7. Remplir le fichier local (jamais commité) :
   ```bash
   cp .env.example .env && chmod 600 .env   # puis éditer PISTE_CLIENT_ID / PISTE_CLIENT_SECRET
   python3 -I -m piste.check                # diagnostic complet
   ```
   (Si `-I` empêche l'import local, lancer `python3 -m piste.check`.)

Dites-moi « c'est fait » : je lance le diagnostic et j'enchaîne sur le serveur MCP. Ne collez jamais le secret dans le chat ; dans une session cloud, je peux plutôt demander un enregistrement sécurisé du secret.

Après ça : si le diagnostic échoue sur un endpoint, c'est probablement un chemin d'API à ajuster d'après le Swagger de votre application PISTE (je corrige alors le client).
