# vericite_app.py – VeriCite: Immutable Source Verification Blockchain (Flask, Vercel)

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4

CHAIN_FILE = 'vericite_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, url, hash_summary, author, validator, tags, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.url = url
        self.hash_summary = hash_summary
        self.author = author
        self.validator = validator
        self.tags = tags
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class VeriCite:
    difficulty = 3

    def __init__(self):
        self.queue = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "", "Genesis", "System", "System", [], "0")]

    def last_block(self):
        return self.chain[-1]

    def submit_source(self, url, hash_summary, author, validator, tags):
        source_id = str(uuid4())
        self.queue.append({
            'url': url,
            'hash_summary': hash_summary,
            'author': author,
            'validator': validator,
            'tags': tags
        })
        return source_id

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * VeriCite.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * VeriCite.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine(self):
        if not self.queue:
            return False
        data = self.queue.pop(0)
        block = Block(
            len(self.chain), time.time(), data['url'], data['hash_summary'],
            data['author'], data['validator'], data['tags'], self.last_block().hash
        )
        proof = self.proof_of_work(block)
        if self.add_block(block, proof):
            return block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

ledger = VeriCite()

@app.route('/')
def explorer():
    html = """
    <html><head><title>VeriCite</title><style>
    body { font-family: sans-serif; padding: 20px; background: #f9f9f9; }
    .block { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>📚 VeriCite – Source Verification Chain</h1>
    {% for block in chain %}
    <div class="block">
        <h3>Block #{{ block.index }}</h3>
        <p><b>URL:</b> {{ block.url }}</p>
        <p><b>Hash Summary:</b> {{ block.hash_summary }}</p>
        <p><b>Author:</b> {{ block.author }}</p>
        <p><b>Validator:</b> {{ block.validator }}</p>
        <p><b>Tags:</b> {{ block.tags }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=ledger.chain)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    required = ('url', 'hash_summary', 'author', 'validator', 'tags')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    source_id = ledger.submit_source(data['url'], data['hash_summary'], data['author'], data['validator'], data['tags'])
    return jsonify({'message': 'Source queued', 'id': source_id})

@app.route('/mine')
def mine():
    result = ledger.mine()
    return jsonify({'message': f'Block #{result} mined' if result is not False else 'No sources to mine'})

@app.route('/chain')
def chain():
    return jsonify([b.__dict__ for b in ledger.chain])

app = app  # Vercel compatibility
