
# TP 1 : Implémentation d'une Mini Blockchain avec Flask

# Réalisé par : BROUKI Aya 
#               KHAILA Imane 
#               EL OUMNI Nora 

# Objectif : Comprendre le fonctionnement d’une blockchain 
#            (minage, transactions, consensus, registre distribué)

#--------------------------------------------------------------------------------------------------


import hashlib       # Pour le hachage SHA-256
import json          # Pour la sérialisation des blocs
from time import time  # Pour les horodatages des blocs
from uuid import uuid4 # Génération d’un identifiant unique de nœud
from urllib.parse import urlparse  # Pour l’analyse des adresses de nœuds
import requests       # Pour la communication entre nœuds via HTTP
from flask import Flask, jsonify, request  # API REST avec Flask

# Classe principale : Blockchain

class Blockchain:
    def __init__(self):
        # Chaîne principale (liste de blocs)
        self.chain = []

        # Liste temporaire pour stocker les transactions non encore validées
        self.current_transactions = []

        # Ensemble des nœuds (autres serveurs dans le réseau)
        self.nodes = set()

        # Création du bloc "genesis" (le tout premier bloc)
        self.new_block(previous_hash='1', proof=100)


    # Création d’un nouveau bloc dans la chaîne

    def new_block(self, proof, previous_hash=None):
       
        # Crée un nouveau bloc et l'ajoute à la blockchain.
        
        block = {
            'index': len(self.chain) + 1,           # Position du bloc
            'timestamp': time(),                    # Date/heure de création
            'transactions': self.current_transactions,  # Liste des transactions validées
            'proof': proof,                         # Preuve de travail
            'previous_hash': previous_hash or self.hash(self.chain[-1]), # Lien vers le bloc précédent
        }

        # Réinitialiser les transactions en attente
        self.current_transactions = []

        # Ajouter le bloc à la chaîne
        self.chain.append(block)
        return block


    # Ajout d’une nouvelle transaction

    def new_transaction(self, sender, recipient, amount):
    
        # Crée une nouvelle transaction qui sera incluse dans le prochain bloc.
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # Retourne l’index du bloc qui contiendra cette transaction
        return self.last_block['index'] + 1


    # Hachage d’un bloc avec SHA-256

    @staticmethod
    def hash(block):
        
        # Génère le hachage SHA-256 d’un bloc.
        
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # Accès au dernier bloc

    @property
    def last_block(self):
        return self.chain[-1]

    # Algorithme de preuve de travail (Proof of Work)
 
    def proof_of_work(self, last_proof):
        
        # Trouve un nombre (proof) tel que le hachage de (last_proof + proof) commence par '0000'.
        
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    # Vérifie la validité d’une preuve

    @staticmethod
    def valid_proof(last_proof, proof):
        
        # Vérifie si la combinaison (last_proof, proof) est valide.
       
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # Difficulté fixée : les 4 premiers caractères doivent être "0000"
        return guess_hash[:4] == "0000"

    # Enregistrement d’un nouveau nœud

    def register_node(self, address):
        
        # Ajoute un nouveau nœud au réseau.
       
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Adresse de nœud invalide')

    # Vérification de la validité d’une chaîne

    def valid_chain(self, chain):
        
        # Vérifie si une blockchain donnée est valide :
        # - Chaque bloc référence bien le précédent
        # - Chaque preuve de travail est correcte
       
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'⛓️ Vérification du bloc {current_index}...')

            # Vérifier le lien entre les blocs
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Vérifier la preuve de travail
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    # Consensus : résolution des conflits

    def resolve_conflicts(self):
      
        # Implémente le mécanisme de consensus :
        # - Remplace notre chaîne par la plus longue chaîne valide trouvée dans le réseau.
        
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    # Si la chaîne trouvée est plus longue et valide → on la remplace
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except requests.exceptions.RequestException:
                continue

        if new_chain:
            self.chain = new_chain
            return True

        return False

# Création de l’application Flask (API REST)

app = Flask(__name__)

# Identifiant unique pour le nœud actuel
node_identifier = str(uuid4()).replace('-', '')

# Instanciation de notre blockchain
blockchain = Blockchain()

#  Route : Miner un nouveau bloc

@app.route('/mine', methods=['GET'])
def mine():
    
    # Exécute le processus de minage :
    # - Calcule une preuve de travail valide
    # - Crée une transaction de récompense (1 unité)
    # - Forge un nouveau bloc
   
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Récompense du mineur (transaction spéciale)
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)

    # Création du nouveau bloc
    block = blockchain.new_block(proof)

    response = {
        'message': "Nouveau bloc miné ",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# Route : Ajouter une transaction

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    
    # Crée une nouvelle transaction envoyée au réseau.
  
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Champs manquants', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction ajoutée au bloc {index}'}
    return jsonify(response), 201

# Route : Obtenir la blockchain complète

@app.route('/chain', methods=['GET'])
def full_chain():
    
    # Retourne la blockchain entière et sa longueur.
    
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

#  Route : Enregistrer de nouveaux nœuds

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    
    # Enregistre une ou plusieurs adresses de nœuds.
    
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Erreur : fournir une liste de nœuds valides", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Nœuds ajoutés',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

# Route : Résolution des conflits (Consensus)

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    
    # Force le nœud à vérifier les autres chaînes et adopter la plus longue valide.
    
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'La chaîne a été remplacée par une plus longue valide ',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Notre chaîne est déjà la plus longue',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

# Lancement du serveur Flask

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='Port du serveur')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
