# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import multiprocessing
import random
from ._hash import Sha256


class Miner:
    def __init__(self, info=None, dif=3, byte_length=64):
        """
        This class creates a Proof of Work BlockChain (PoW) of the incoming information of the block.
        :param info: Raw Information of the block.
        :param dif: The current difficulty of the BlockChain.
        :param byte_length: Bytes reserved to the fingerprint defined in the protocol.
        """
        if info:
            self.info = info.encode()
        else:
            self.info = None
        self.dif = byte_length - dif
        self._hl = byte_length
        self.block = None
        self.hash = None

    def set_info(self, info, dif=None):
        """
        This method sets the information of the block.
        :param info: Information.
        :param dif:  Difficulty of the blockchain.
        :return: The called object.
        """
        self.info = info
        if dif is not None:
            self.dif = self._hl - dif
        return self

    @staticmethod
    def compute_hash(block):
        """
        This function computes the hash of the preamble.
        :param block: The block to be computed.
        :return: The hash of the block.
        """
        return Sha256(block)

    def validate_hash(self, block):
        """
        This function computes the hash of the information provided.
        :param block: The block to be modified.
        :return: True if the block is valid. False if not.
        """
        this_hash_len = len(self.compute_hash(block))
        if self.dif >= this_hash_len:
            print(f'Valid hash found: {self.compute_hash(block)}\nfor block: {block}')
            return True
        else:
            return False

    def compute_random_hash(self):
        """
        Computes a random preamble and tries the hash.
        :return: True if the preamble is valid. False if not.
        """
        preamble = random.randbytes(self._hl)
        block = preamble + self.info
        if self.validate_hash(block):
            self.hash = self.compute_hash(block)
            self.block = block
            return True
        else:
            return False

    def work(self, chunk: tuple[int, int], _q: multiprocessing.Queue = None):
        """
        This method makes the miner compute all the hashes inside a chunk.
        :param chunk: A tuple with the chunk start and the chunk end.
        :param _q: Optional multiprocessing Queue.
        :return: True is the solution is found, else False.
        """
        chunk_init = int(chunk[0])
        chunk_ending = int(chunk[1])
        print(f'\t[-] Worker: Creating chunk {chunk_init} - {chunk_ending}.')
        for chunk_hashable in range(chunk_init, chunk_ending):
            preamble = chunk_hashable.to_bytes(self._hl, 'big')
            block = preamble + self.info
            if self.validate_hash(block):
                print(f'\t[-] Solution found in preamble {chunk_hashable}.')
                self.hash = self.compute_hash(block)
                self.block = block
                if _q is not None:
                    _q.put(self)
                return self
        if _q is not None:
            _q.put(False)
        print(f'\t[-] Solution NOT found in chunk {chunk_init} - {chunk_ending}.')
        return False

    def __hash__(self):
        _valid_preamble = False
        while not _valid_preamble:
            _valid_preamble = self.compute_random_hash()
        return int.from_bytes(self.hash.hash_byt, 'big')
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
