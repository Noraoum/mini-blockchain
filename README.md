# Exécution et tests
Pour tester les endpoints, exécutez chaque commande dans le terminal séparément.

# %% Cellule 1 : Lancer le premier nœud (port 5000)
# Description : Cette cellule démarre le nœud principal de votre blockchain
!python app.py -p 5000
# %% Fin cellule 1

# %% Cellule 2 : Tester les endpoints sur le nœud 5000
# Description : Affiche la blockchain complète sur le nœud principal
!curl http://127.0.0.1:5000/chain
# %% Fin cellule 2

# %% Cellule 3 : Ajouter une transaction (POST /transactions/new)
# Description : Créer une transaction de Alice vers Bob pour un montant de 5
!curl -X POST http://127.0.0.1:5000/transactions/new \
-H "Content-Type: application/json" \
-d "{\"sender\":\"Alice\",\"recipient\":\"Bob\",\"amount\":5}"
# %% Fin cellule 3

# %% Cellule 4 : Miner un bloc (GET /mine)
# Description : Valider les transactions et créer un nouveau bloc
!curl http://127.0.0.1:5000/mine
# %% Fin cellule 4

# %% Cellule 5 : Lancer d’autres nœuds pour simuler un réseau décentralisé
# Description : Ouvrez un deuxième terminal ou onglet et lancez les commandes suivantes
!python app.py -p 5001
!python app.py -p 5002
# %% Fin cellule 5

# %% Cellule 6 : Enregistrer des nœuds entre eux
# Description : Faire connaître les nœuds 5001 et 5002 au nœud principal (5000)
!curl -X POST http://127.0.0.1:5000/nodes/register \
-H "Content-Type: application/json" \
-d "{\"nodes\":[\"http://127.0.0.1:5001\",\"http://127.0.0.1:5002\"]}"
# %% Fin cellule 6
