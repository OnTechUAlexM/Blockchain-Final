import hashlib
from time import time
from datetime import datetime
import json


class Blockchain:
    _difficulty_level = "0" * 5

    def __init__(self):
        self.chain = list()
        self.transactions = list()
        gen_hash = self.hash_block('genesis_block')
        self.append_block(
            prev_hash=gen_hash,
            nonce=self.pow(0, gen_hash, [])
        )

    @classmethod
    def with_difficulty(cls, val: str):
        assert isinstance(val, str), "Difficulty must be a string consisting of only 0's"
        assert val.count('0') == len(val), "Difficulty must only consist of 0's"
        bc = cls()
        bc._difficulty_level = val
        bc.__init__()
        return bc

    @property
    def last_block(self):
        return self.chain[-1]

    # Hashes the next block
    def hash_block(self, block):
        block_encoder = json.dumps(block, sort_keys=True).encode()
        hs = hashlib.sha512(block_encoder)
        return hs.hexdigest()

    # Appends a new block to the chain
    def append_block(self, prev_hash, nonce) -> dict:
        block = {
            'index': len(self.chain),
            'timestamp': datetime.utcnow().strftime('%d-%b-%y %H:%M:%S'),
            'transaction': self.transactions,
            'nonce': nonce,
            'prev_hash': prev_hash
        }
        self.transactions = list()
        self.chain.append(block)
        return block

    # Add a transaction
    def add_transaction(self, sender, recipient, cost, vin, make: str, model: str, year: str, condition: str, mileage: float):
        self.transactions.append({
            'vin': vin,
            'make': make,
            'model': model,
            'year': year,
            'condition': condition,
            'mileage': mileage,
            'cost': cost,
            'recipient': recipient,
            'sender': sender
        })
        return self.last_block

    # Proof of work
    def pow(self, index: int, prev_hash: str, transactions: list):
        nonce = 0
        while self.validate_proof(index, prev_hash, transactions, nonce) is False:
            nonce += 1
        return nonce

    def validate_proof(self, index, prev_hash, transactions, nonce):
        content = f'{index}{prev_hash}{transactions}{nonce}'
        c_hash = self.hash_block(content)
        return c_hash.startswith(self._difficulty_level)


if __name__ == '__main__':
    b = Blockchain()