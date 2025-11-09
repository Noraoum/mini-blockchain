# 🪙 Mini Blockchain avec Python & Flask

## 🎯 Objectif du projet

L’objectif de ce TP est de comprendre le fonctionnement d’une **blockchain** en la construisant à partir de zéro avec **Python** et **Flask**.  
Nous avons cherché à reproduire les principes fondamentaux suivants :
- Le **hachage cryptographique** des blocs (SHA-256)
- Le **minage** de nouveaux blocs avec une **preuve de travail** (Proof of Work)
- La **création et validation de transactions**
- Le **stockage distribué** et la **synchronisation entre plusieurs nœuds**
- La mise en place d’une **API REST** pour interagir avec la blockchain

---

## ⚙️ Fonctionnalités principales

- 🔗 Création et gestion d’une **blockchain** complète
- 💸 Envoi et ajout de **transactions**
- ⛏️ **Minage** de nouveaux blocs avec récompense automatique
- 🌍 Ajout de **plusieurs nœuds** pour simuler un réseau décentralisé
- 🤝 **Consensus** entre nœuds pour garantir la validité de la chaîne
- 📡 API REST simple et intuitive pour interagir avec le réseau

---

## 🧩 Ce que nous avons réalisé

1. Création d’une classe `Blockchain` gérant :
   - Les blocs, transactions et preuves de travail
   - Le hachage SHA-256 pour assurer l’intégrité de la chaîne
2. Mise en place d’un **serveur Flask** pour exposer l’API REST
3. Ajout de routes permettant :
   - D’ajouter une transaction (`/transactions/new`)
   - De miner un bloc (`/mine`)
   - D’afficher la blockchain (`/chain`)
   - D’enregistrer de nouveaux nœuds (`/nodes/register`)
   - De résoudre les conflits entre nœuds (`/nodes/resolve`)
4. Simulation d’un **réseau décentralisé** avec plusieurs nœuds (5000, 5001, 5002...)

---

## 🧪 Exécution et tests

> 💡 Tous les exemples de commandes pour tester les endpoints se trouvent ci-dessous.  
> Il suffit de les exécuter dans le terminal.

### 1️⃣ Lancer le premier nœud (port 5000)
```bash
python app.py -p 5000
2️⃣ Tester les endpoints sur le nœud 5000
Afficher la blockchain complète :

bash
Copier le code
curl http://127.0.0.1:5000/chain
3️⃣ Ajouter une transaction (POST /transactions/new)
bash
Copier le code
curl -X POST http://127.0.0.1:5000/transactions/new ^
-H "Content-Type: application/json" ^
-d "{\"sender\":\"Alice\",\"recipient\":\"Bob\",\"amount\":5}"
4️⃣ Miner un bloc (GET /mine)
bash
Copier le code
curl http://127.0.0.1:5000/mine
5️⃣ Lancer d’autres nœuds (pour simuler un réseau décentralisé)
Ouvre un nouveau terminal pour chaque nœud :

bash
Copier le code
python app.py -p 5001
python app.py -p 5002
6️⃣ Enregistrer les nœuds entre eux
Faire connaître les nœuds 5001 et 5002 au nœud principal (5000) :

bash
Copier le code
curl -X POST http://127.0.0.1:5000/nodes/register ^
-H "Content-Type: application/json" ^
-d "{\"nodes\":[\"http://127.0.0.1:5001\",\"http://127.0.0.1:5002\"]}"
7️⃣ Synchroniser la blockchain entre les nœuds
bash
Copier le code
curl http://127.0.0.1:5000/nodes/resolve