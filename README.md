# Quiz de mots rares

Mini-jeu qui pioche un mot rare dans le [dictionnaire du français difficile
de webnext.fr](https://webnext.fr/dictionnaire-du-francais-difficile-mots-rares-et-recherches-1016.html)
et te fait choisir sa définition parmi 3.

## Jouer en ligne

Une fois le dépôt poussé sur GitHub avec **GitHub Pages** activé (voir plus
bas), le jeu est accessible directement à cette adresse (à adapter) :

```
https://<TON_PSEUDO_GITHUB>.github.io/<NOM_DU_DEPOT>/
```

Ce lien ouvre directement le jeu dans le navigateur, aucune installation
nécessaire pour un joueur.

## Régénérer la liste des mots

Le dépôt contient un `mots.json` de démonstration (2 mots). Pour récupérer
l'intégralité du dictionnaire (~3500 mots) :

```bash
pip install requests beautifulsoup4
python build_data.py
```

Cela écrit un `mots.json` complet à côté du script. Il ne reste plus qu'à
commiter et pousser ce fichier :

```bash
git add mots.json
git commit -m "Mise à jour des mots"
git push
```

Le site sur GitHub Pages se met à jour automatiquement après le push
(généralement en moins d'une minute).

## Mettre le projet sur GitHub (première fois)

1. Crée un nouveau dépôt vide sur https://github.com/new (par exemple
   `quiz-mots-rares`), **sans** cocher "Add a README" (on en a déjà un).
2. Dans ce dossier, exécute :

   ```bash
   git init
   git add .
   git commit -m "Premier commit"
   git branch -M main
   git remote add origin https://github.com/<TON_PSEUDO_GITHUB>/<NOM_DU_DEPOT>.git
   git push -u origin main
   ```

3. Sur GitHub, va dans **Settings > Pages** du dépôt, choisis la branche
   `main` (dossier `/ (root)`), puis **Save**.
4. Après une minute, le jeu est en ligne à l'adresse indiquée en haut de
   cette page.

## Structure du dépôt

- `index.html` — le jeu (HTML/CSS/JS autonome, charge `mots.json`).
- `mots.json` — les mots/définitions/citations utilisés par le jeu.
- `build_data.py` — scrape webnext.fr et régénère `mots.json`.
