import hvac

from src.kms.base import KMSInterface


class VaultKMS(KMSInterface):
    """HashiCorp Vault KMS provider."""

    def __init__(
        self,
        url: str,
        token: str,
        mount_point: str = "transit",
    ) -> None:
        self.client = hvac.Client(url=url, token=token)
        self.mount = mount_point

    def generate_key(self, key_id: str) -> None:
        self.client.secrets.transit.create_key(
            name=key_id,
            mount_point=self.mount,
        )

    def get_signer(self, key_id: str):
        return lambda data: self.client.secrets.transit.sign_data(
            name=key_id,
            input=data,
            mount_point=self.mount,
        )["data"]["signature"]

    def encrypt(self, key_id: str, plaintext: bytes) -> bytes:
        result = self.client.secrets.transit.encrypt_data(
            name=key_id,
            plaintext=plaintext.hex(),
            mount_point=self.mount,
        )
        return bytes.fromhex(result["data"]["ciphertext"])

    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        result = self.client.secrets.transit.decrypt_data(
            name=key_id,
            ciphertext=ciphertext.hex(),
            mount_point=self.mount,
        )
        return bytes.fromhex(result["data"]["plaintext"])
