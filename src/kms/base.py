from abc import ABC, abstractmethod


class KMSInterface(ABC):
    """Abstract Key Management Service interface."""

    @abstractmethod
    def generate_key(self, key_id: str) -> None:
        """Generate a new key with the given key_id."""
        pass

    @abstractmethod
    def get_signer(self, key_id: str):
        """Return a callable that signs bytes."""
        pass

    @abstractmethod
    def encrypt(self, key_id: str, plaintext: bytes) -> bytes:
        """Encrypt data using key_id."""
        pass

    @abstractmethod
    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        """Decrypt data using key_id."""
        pass
