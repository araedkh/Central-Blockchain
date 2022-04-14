import time
from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_bin import hex_to_bin
from backend.config import MINE_RATE

GENESIS_DATA = {
    'number': 0,
    'timestamp': 1,
    'timerec': '0',
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:


    def __init__(self, number, timestamp, timerec, last_hash, hash, data, difficulty, nonce):
        self.number = number
        self.timestamp = timestamp
        self.timerec = timerec
        self.hash = hash
        self.last_hash = last_hash
        self.data = data
        self.difficulty = difficulty  # Number of leading zeros in the block hash.
        self.nonce = nonce  # Number of iterations required to reach the valid hash.

    def __repr__(self):  # This method is required to print out the class value of the block.
        return (
            f'Block-number: {self.number}\n'
            f'Block-time recorded: {self.timerec}\n'  # Prints the date and time of the block entry.
            f'Block-timestamp: {self.timestamp}\n'
            f'Block-hash: {self.hash}\n'
            f'Block-last_hash: {self.last_hash}\n'
            f'Block-data: {self.data}\n'
            f'Difficulty: {self.difficulty}\n'
            f'Nonce: {self.nonce}\n\n'
        )

    def __eq__(self, other):
       
        return self.__dict__ == other.__dict__

    def to_json(self):

        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):

        number = last_block.number + 1
        timestamp = time.time_ns()  # Returns time in nanoseconds .
        last_hash = last_block.hash
        difficulty = Block.adjust_diff(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_bin(hash)[
              0:difficulty] != '0' * difficulty:

            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_diff(last_block,
                                           timestamp)  # Difficulty will get itself adjusted according to current block timestamp.
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        timerec = time.asctime()  # Returns time in form of string.

        return Block(number, timestamp, timerec, last_hash, hash, data, difficulty, nonce)

    @staticmethod
    def genesis():

        return Block(**GENESIS_DATA)


    @staticmethod
    def from_json(block_json):

        return Block(**block_json)

    @staticmethod
    def adjust_diff(last_block, new_timestamp):

        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def isblockvalid(last_block, block):


        if block.last_hash != last_block.hash:
            raise Exception("The block hash is invalid")

        if hex_to_bin(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The PoW requirement was not met')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The difficulty level must only adjusted by one')

        reconst_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce
        )

        if block.hash != reconst_hash:
            raise Exception('The block hash must be correct')


def main():
    gen_block = Block.genesis()
    good_block = Block.mine_block(gen_block, 'Hello')
    # bad_block.last_hash = 'Fished the hash'
    try:
        Block.isblockvalid(gen_block, good_block)

    except Exception as e:
        print(f'isblockvalid:{e}')


if __name__ == '__main__':
    main()