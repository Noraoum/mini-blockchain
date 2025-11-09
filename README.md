# 🪙 Mini Blockchain avec Python & Flask

## 🎯 Objectif du projet

L’objectif de ce TP est de comprendre le fonctionnement d’une **blockchain** en la construisant à partir de zéro avec **Python** et **Flask**.  
Nous avons reproduit les concepts clés suivants :
- Hachage SHA-256 des blocs
- Minage avec preuve de travail (Proof of Work)
- Gestion des transactions
- Réseau décentralisé avec plusieurs nœuds
- API REST pour interagir avec la blockchain

---

## ⚙️ Fonctionnalités principales

- 🔗 Gestion complète d’une blockchain
- 💸 Ajout de transactions
- ⛏️ Minage avec récompense
- 🌍 Réseau décentralisé et synchronisation
- 🤝 Consensus entre nœuds
- 📡 API REST simple pour tester et interagir

---

## 🧩 Ce que nous avons réalisé

1. Classe `Blockchain` avec blocs, transactions et preuve de travail
2. Serveur Flask pour exposer l’API REST
3. Routes pour :
   - Ajouter une transaction (`/transactions/new`)
   - Miner un bloc (`/mine`)
   - Afficher la blockchain (`/chain`)
   - Ajouter des nœuds (`/nodes/register`)
   - Résoudre les conflits (`/nodes/resolve`)
4. Simulation d’un réseau décentralisé avec plusieurs nœuds

---

## 🧪 Exécution et tests

> Toutes les commandes pour tester les endpoints et simuler le réseau se trouvent ici.

1️⃣ Lancer le premier nœud (port 5000)
```bash
python app.py -p 5000

2️⃣ Tester les endpoints sur le nœud 5000.
Afficher la blockchain complète :
```bash
curl http://127.0.0.1:5000/chain

3️⃣ Ajouter une transaction (POST /transactions/new).
```bash
curl -X POST http://127.0.0.1:5000/transactions/new ^
-H "Content-Type: application/json" ^
-d "{\"sender\":\"Alice\",\"recipient\":\"Bob\",\"amount\":5}"

4️⃣ Miner un bloc (GET /mine).
```bash
curl http://127.0.0.1:5000/mine

5️⃣ Lancer d’autres nœuds (simuler un réseau décentralisé).
Ouvre un deuxième terminal (ou onglet) et lance chaque nœud :
```bash
python app.py -p 5001
python app.py -p 5002

6️⃣ Enregistrer les nœuds entre eux.
Faire connaître les nœuds 5001 et 5002 au nœud principal (5000) :
```bash
curl -X POST http://127.0.0.1:5000/nodes/register ^
-H "Content-Type: application/json" ^
-d "{\"nodes\":[\"http://127.0.0.1:5001\",\"http://127.0.0.1:5002\"]}"

7️⃣ Synchroniser la blockchain entre les nœuds.
```bash
curl http://127.0.0.1:5000/nodes/resolve
