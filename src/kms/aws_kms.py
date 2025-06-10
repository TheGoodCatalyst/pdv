import boto3

from src.kms.base import KMSInterface


class AWSKMS(KMSInterface):
    """AWS KMS provider using boto3."""

    def __init__(self, region_name: str) -> None:
        self.client = boto3.client("kms", region_name=region_name)

    def generate_key(self, key_id: str) -> None:
        resp = self.client.create_key(Description=key_id)
        key_arn = resp["KeyMetadata"]["KeyId"]
        self.client.create_alias(
            AliasName=f"alias/{key_id}",
            TargetKeyId=key_arn,
        )

    def get_signer(self, key_id: str):
        return lambda data: self.client.sign(
            KeyId=f"alias/{key_id}",
            Message=data,
            MessageType="RAW",
        )["Signature"]

    def encrypt(self, key_id: str, plaintext: bytes) -> bytes:
        resp = self.client.encrypt(
            KeyId=f"alias/{key_id}",
            Plaintext=plaintext,
        )
        return resp["CiphertextBlob"]

    def decrypt(self, key_id: str, ciphertext: bytes) -> bytes:
        resp = self.client.decrypt(CiphertextBlob=ciphertext)
        return resp["Plaintext"]
