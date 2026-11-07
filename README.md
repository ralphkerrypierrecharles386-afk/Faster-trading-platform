# Edit — Plateforme IA de Trading Automatique Professionnelle

Base d'architecture Python modulaire pour une plateforme de trading
algorithmique avec moteur d'analyse technique (Smart Money Concepts),
gestion du risque paramétrable, backtesting et tableau de bord Streamlit.

> 🚀 **Application en ligne** : accessible en un clic via le navigateur,
> sur PC comme sur mobile — voir la section
> [Accès direct à l'application](#-accès-direct-à-lapplication).

## 📥 Téléchargement du code source

- **Code source complet (ZIP)** : [Faster-trading-platform-main.zip](https://github.com/ralphkerrypierrecharles386-afk/Faster-trading-platform/archive/refs/heads/main.zip)
- **Code source complet (TAR.GZ)** : [Faster-trading-platform-main.tar.gz](https://github.com/ralphkerrypierrecharles386-afk/Faster-trading-platform/archive/refs/heads/main.tar.gz)
- **Page GitHub du projet** : https://github.com/ralphkerrypierrecharles386-afk/Faster-trading-platform

Ces liens fonctionnent immédiatement : un clic télécharge le code source
(dépôt public, aucune connexion GitHub requise).

## 🚀 Accès direct à l'application

> ⏳ **L'URL de l'application en ligne sera ajoutée ici après le
> déploiement** (voir la procédure ci-dessous). Ce lien n'existe pas
> encore — ne pas le diffuser tant qu'il n'a pas été complété.

### Comment déployer (5 minutes)

**Étape 1 — Fusionner la Pull Request**

Ouvrez https://github.com/ralphkerrypierrecharles386-afk/Faster-trading-platform/pull/2
et cliquez sur **Merge pull request**. Sans cette étape, le fichier
`dashboard/app.py` n'existe pas sur `main` et le déploiement échouera.

**Étape 2 — Déployer sur Streamlit Community Cloud**

1. Ouvrez https://share.streamlit.io et connectez-vous avec votre compte GitHub.
2. Cliquez **New app**.
3. Sélectionnez :
   - **Repository** : `ralphkerrypierrecharles386-afk/Faster-trading-platform`
   - **Branch** : `main`
   - **Main file path** : `dashboard/app.py`
4. Cliquez **Deploy**. Après 1-2 minutes, Streamlit affiche l'URL de
   votre application (`https://<nom-choisi>.streamlit.app`).
5. Remplacez le bloc ⏳ ci-dessus par :
   ```markdown
   - **Application en ligne** : [https://VOTRE-URL.streamlit.app](https://VOTRE-URL.streamlit.app)
   ```
   C'est le lien « clic et ça ouvre » à partager — un clic ouvre
   l'application directement dans le navigateur, sur PC et mobile.

### Lancer en local (alternative)

```bash
# 1. Télécharger ou cloner le code source
git clone https://github.com/ralphkerrypierrecharles386-afk/Faster-trading-platform.git
cd Faster-trading-platform

# 2. Installer les dépendances (Python 3.10+ requis)
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run dashboard/app.py
```

## Structure du projet

```
Faster-trading-platform/
├── config/            # Configuration centralisée (settings.py)
├── core/              # Base de données (SQLAlchemy)
├── dashboard/         # Tableau de bord Streamlit (app.py)
├── data/              # Stockage (base SQLite, créée au premier lancement)
└── requirements.txt   # Dépendances Python
```

## Installation locale

```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

## Feuille de route (statut de cette base)

| Étape | Contenu | Statut |
|---|---|---|
| 1. Architecture | Structure de dossiers, config, DB | ✅ posé |
| 2. Moteur d'analyse | BOS, CHoCH, Order Blocks, FVG, liquidité | ✅ v2 durcie |
| 3. Gestion du risque | Position sizing, DD max, R:R min | ✅ v1 fonctionnelle |
| 4. Backtesting | Moteur event-driven, métriques | ✅ v1 |
| 5. Tableau de bord | Streamlit : équité, trades, signaux | ✅ v1 |
| 6. Déploiement cloud | Streamlit Community Cloud | ⏳ prêt à déployer |

## Avertissement

Le trading algorithmique comporte un risque de perte en capital. Ce code
est une base technique ; il ne constitue ni un conseil financier ni une
garantie de performance. Toute mise en production réelle doit être
précédée de tests approfondis en compte démo.
