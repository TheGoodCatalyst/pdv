import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives import hashes

from src.kms.base import KMSInterface


class LocalKMS(KMSInterface):
    """Software-based KMS stub storing keys in-memory (for dev)."""

    def __init__(self) -> None:
        self._keys: dict[str, bytes] = {}

    def generate_key(self, key_id: str) -> None:
        key = AESGCM.generate_key(bit_length=256)
        self._keys[key_id] = key

    def get_signer(self, key_id: str):
        key = self._keys[key_id]

        def signer(message: bytes) -> bytes:
            h = HMAC(key, hashes.SHA256())
            h.update(message)
            return h.finalize()

        return signer

    def encrypt(self, key_id: str, plaintext: bytes) -> bytes:
        key = self._keys[key_id]
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        return nonce + aesgcm.encrypt(nonce, plaintext, None)

    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        key = self._keys[key_id]
        aesgcm = AESGCM(key)
        nonce, ct = ciphertext[:12], ciphertext[12:]
        return aesgcm.decrypt(nonce, ct, None)
