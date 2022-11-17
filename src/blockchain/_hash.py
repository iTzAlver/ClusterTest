# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                                                           #
#   This file was created by: Alberto Palomo Alonso         #
# Universidad de Alcalá - Escuela Politécnica Superior      #
#                                                           #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
# Import statements:
import hashlib


# -----------------------------------------------------------
class Sha256:
    def __init__(self, byte_stream: bytes):
        """
        Creates a Sha256 util class for haslib. Has the following attributes:
            * hash_ex = The hex representation of the hash.
            * hash_byt = The byte representation of the hash.
            * rank = The difficulty rank of the hash.
        The class supports the len() method for diff rank extraction and arithmetic add (:bytes = :self + :bytes).
        :param byte_stream: The input bytes to be hashed.
        """
        _hash = hashlib.sha256(byte_stream)
        self.hash_hex = _hash.hexdigest()
        self.hash_byt = _hash.digest()
        self.rank = len(self)

    def __len__(self):
        rank = len(self.hash_hex)
        for char in self.hash_hex:
            if char == '0':
                rank -= 1
            else:
                return rank
        return rank

    def __repr__(self):
        return self.hash_hex.__repr__()

    def __add__(self, other):
        return self.hash_byt + other
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
#                        END OF FILE                        #
# - x - x - x - x - x - x - x - x - x - x - x - x - x - x - #
