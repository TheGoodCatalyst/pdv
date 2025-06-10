import pytest

from src.kms.base import KMSInterface
from src.kms.local_kms import LocalKMS


@pytest.fixture
def kms() -> LocalKMS:
    kms = LocalKMS()
    return kms


def test_local_kms_implements_interface(kms):
    assert isinstance(kms, KMSInterface)


def test_encrypt_roundtrip(kms):
    key_id = "test"
    kms.generate_key(key_id)
    plaintext = b"secret-data"
    ciphertext = kms.encrypt(key_id, plaintext)
    assert ciphertext != plaintext
    decrypted = kms.decrypt(key_id, ciphertext)
    assert decrypted == plaintext


def test_signer_not_implemented(kms):
    kms.generate_key("sig")
    with pytest.raises(NotImplementedError):
        kms.get_signer("sig")
