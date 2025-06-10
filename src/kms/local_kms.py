import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from src.kms.base import KMSInterface


class LocalKMS(KMSInterface):
    """Software-based KMS stub storing keys in-memory (for dev)."""

    def __init__(self) -> None:
        self._keys: dict[str, bytes] = {}

    def generate_key(self, key_id: str) -> None:
        key = AESGCM.generate_key(bit_length=256)
        self._keys[key_id] = key

    def get_signer(self, key_id: str):
        raise NotImplementedError("LocalKMS does not support signing")

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
