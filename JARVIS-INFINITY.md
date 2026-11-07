# J.A.R.V.I.S. ∞ — Assistant Personnel Intelligent de Nouvelle Génération

> **Just A Rather Very Intelligent System — Infinite Edition**
> Interface web autonome 100 % locale (HTML/CSS/JS, aucune dépendance à installer), conçue comme un poste de pilotage personnel inspiré de JARVIS (Iron Man), avec moteur conversationnel, moteur vocal, mémoire intelligente, analyse financière et trading temps réel.

---

## 📦 Téléchargement / Accès

| Ressource | URL |
|---|---|
| **Application J.A.R.V.I.S. ∞ (artefact live)** | https://app.ashna.ai/artifact/6aef8262c5985b0018f0f883 |
| **Ce dépôt (source + docs)** | https://github.com/ralphkerrypierrecharles386-afk/Faster-trading-platform |
| **Dépôt plateforme Python (privé)** | `ralphkerrypierrecharles386-afk/Quaint-IA-trading` |

L'application est une **page HTML unique auto-contenue** : ouvrez l'artefact ci-dessus dans Chrome ou Edge et tout fonctionne hors ligne (voix, mémoire, paper trading, calculs financiers). Les flux Binance publics sont chargés en direct, sans clé API.

---

## 🗺️ Les 10 phases livrées

| Phase | Module | Contenu |
|---|---|---|
| 1–3 | Audit + Architecture + Interface | Noyau IA à 7 états (Idle → Listening → Processing → Speaking → Executing → Completed / Error), design holographique (noir profond, cyan, bleu électrique), Command Center |
| 4 | Moteur conversationnel | Pipeline 5 étapes (intention → contexte → décomposition → routage → réponse), classification d'intention locale, contexte glissant 10 échanges, couche fournisseurs local/distant avec fallback |
| 5 | Moteur vocal avancé | Commandes vocales personnalisables, détection de fin de parole (silence réglable), barge-in réel, diagnostics micro (VU-mètre, permissions), historique vocal enrichi, wake-word honnête, export/import |
| 6 | Mémoire intelligente | 4 types hiérarchiques (épisodique/sémantique/procédurale/profil), extraction assistée avec confirmation, profil utilisateur, rappel contextuel scoré, recherche avancée, décroissance configurable |
| 7 | Analyse financière | Watchlist, calculs quantitatifs locaux (volatilité, max drawdown, RSI, PER, ROE…), journal d'événements qualitatifs (rumeurs/presse/judiciaire/réglementaire), distinction fait vs rumeur, pression informationnelle, backend de données branchable |
| 8 | Trading temps réel | WebSocket public Binance (prix sub-seconde), chandeliers, carnet d'ordres depth20, paper trading rigoureux contre prix réels, ordres réels uniquement via backend signataire, arrêt d'urgence global |
| 9 | MT4 / MT5 / TradingView | Voie EA bridge local (ws://localhost:8890) ou cloud type MetaApi ; widget officiel TradingView ; réception webhooks via backend relais ; politique d'exécution 3 modes avec triple garde |
| 10 | Tests & diagnostics | Endpoints Binance vérifiés en direct, CI/CD GitHub Pages validé, auto-diagnostic intégré à l'interface |

---

## 🔐 Sécurité — principes non négociables

- **Zéro clé/secret API dans le navigateur** : aucune signature HMAC, aucun token dans le frontend. Les ordres réels passent exclusivement par un backend appartenant à l'utilisateur, qui seul signe (Binance HMAC-SHA256, tokens MetaApi, relais webhooks TradingView).
- **Échappement XSS systématique** de tout texte utilisateur inséré dans le DOM.
- **Confirmations obligatoires** : double confirmation pour tout ordre réel, triple garde (liste blanche + plafond + fréquence) pour l'exécution automatique d'alertes.
- **Distinction permanent fait confirmé vs rumeur** (badges vert/orange) et avertissements légaux : outil d'analyse, pas un conseil en investissement.

---

## 🏗️ Architecture de la couche trading

```
┌─────────────────────────┐      WebSocket public        ┌──────────────────┐
│   J.A.R.V.I.S. ∞ (web)  │◄───────────────────────────►│  Binance (spot)  │
│  - Marchés temps réel    │   wss://stream.binance.com   │  prix/carbet/klines│
│  - Paper trading local   │                              └──────────────────┘
│  - Panneaux MT4/MT5/TV   │      ws://localhost:8890     ┌──────────────────┐
│  - Arrêt d'urgence       │◄───────────────────────────►│  EA bridge MT5   │
└───────────┬─────────────┘   REST :8891/api/v1          │  (terminal PC)   │
            │  fetch POST {order}                          └──────────────────┘
            ▼
┌─────────────────────────┐   signe HMAC-SHA256    ┌──────────────────┐
│  VOTRE backend (Node/   │───────────────────────►│  Binance / brokers│
│  Python, à vous)        │   tokens restent ici   │  (ordres réels)  │
│  - /api/chat            │                        └──────────────────┘
│  - /api/binance/order   │
│  - /api/alerts (webhooks TradingView)             ┌──────────────────┐
│  - /api/financials      │◄──────webhook POST─────│   TradingView    │
└─────────────────────────┘   (relais HTTPS)       │  (alertes Pine)  │
                                                   └──────────────────┘
```

---

## ⚙️ Backend minimal à déployer (côté serveur)

L'interface expose des champs URL pour brancher votre backend :

| Endpoint | Payload reçu | Réponse attendue | Usage |
|---|---|---|---|
| `POST /api/chat` | `{message, context, memories}` | `{reply}` | Moteur conversationnel distant |
| `POST /api/binance/order` | `{symbol, side, type, price, quantity, stopPrice}` | `{orderId, status, executedQty}` | Ordres réels signés |
| `GET /api/binance/status` | — | `{connected, testnet}` | Test connexion |
| `POST /api/financials` | `{tickers, types}` | `{quotes, history, financials, news}` | Données boursières |
| `GET /api/alerts` | — | `[{time, ticker, action, price, qty, status}]` | Relais webhooks TradingView |

Exemple Node.js (signature Binance, secret jamais exposé) :

```js
// POST /api/binance/order
import crypto from 'node:crypto';
app.post('/api/binance/order', async (req, res) => {
  const { symbol, side, type, price, quantity, stopPrice } = req.body;
  const params = new URLSearchParams({
    symbol, side, type,
    quantity: String(quantity),
    timestamp: String(Date.now()),
    recvWindow: '5000',
  });
  if (type === 'LIMIT') { params.set('price', String(price)); params.set('timeInForce', 'GTC'); }
  if (stopPrice) params.set('stopPrice', String(stopPrice));
  const signature = crypto
    .createHmac('sha256', process.env.BINANCE_SECRET)
    .update(params.toString())
    .digest('hex');
  params.set('signature', signature);
  const r = await fetch('https://api.binance.com' + '/api/v3/order?' + params.toString(), {
    method: 'POST',
    headers: { 'X-MBX-APIKEY': process.env.BINANCE_KEY },
  });
  res.status(r.status).json(await r.json());
});
```

---

## 🖥️ Intégration avec la plateforme Python existante (`Quaint-IA-trading`)

La plateforme « Edit » (dépôt privé) et J.A.R.V.I.S. ∞ sont complémentaires :

- Le **backend de J.A.R.V.I.S. ∞** peut être la plateforme Python elle-même : exposer `engine.py` (signaux SMC BOS/CHoCH/OB/FVG) via une petite couche API (FastAPI/Flask) et brancher l'URL dans Paramètres → Moteur conversationnel / Sources de données.
- L'**EA bridge MT5** peut s'appuyer sur `mt5_connector.py` + `order_manager.py` pour relayer ordres et positions via WebSocket local.
- `risk_manager.py` (drawdown journalier, R:R min, max positions) reste la **garde-fous serveur** de toute exécution réelle — jamais contournable depuis le navigateur.

---

## 🚀 Déploiement GitHub Pages (déjà en place)

Le workflow `.github/workflows/static.yml` déploie automatiquement ce dépôt sur GitHub Pages à chaque push sur `main` :

1. Merge de la PR `jarvis-infinity-docs` → `main`
2. Le workflow `pages build and deployment` se déclenche automatiquement
3. L'application est servie à l'URL Pages du dépôt

---

## ⚠️ Avertissements légaux

- Le trading de crypto-actifs, CFD et Forex comporte un **risque élevé de perte en capital**. Ni J.A.R.V.I.S. ∞ ni la plateforme Edit ne constituent un conseil en investissement.
- Les ordres réels ne sont passés que via vos propres ponts/backends, **sous votre entière responsabilité**.
- Les rumeurs peuvent être fausses : vérifiez toujours les sources primaires avant toute décision.

---

*J.A.R.V.I.S. ∞ — conçu et livré avec l'assistant Ashna-X1 (AshnaAI), dans le respect du principe « 100 % réel, aucune donnée inventée, aucun secret dans le navigateur ».*
