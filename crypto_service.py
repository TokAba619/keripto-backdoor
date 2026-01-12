<<<<<<< HEAD
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type

MAGIC = b"SFV1"
SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32  # AES-256


def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64 MB
        parallelism=2,
        hash_len=KEY_LEN,
        type=Type.ID,
    )


def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    return MAGIC + salt + nonce + ciphertext


def decrypt_bytes(blob: bytes, password: str) -> bytes:
    if len(blob) < len(MAGIC) + SALT_LEN + NONCE_LEN + 1:
        raise ValueError("Invalid encrypted file (too small).")

    if blob[:4] != MAGIC:
        raise ValueError("Invalid encrypted file (bad header).")

    salt = blob[4:4 + SALT_LEN]
    nonce = blob[4 + SALT_LEN:4 + SALT_LEN + NONCE_LEN]
    ciphertext = blob[4 + SALT_LEN + NONCE_LEN:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

from file_lockers import is_pdf, lock_pdf

def process_and_encrypt(
    data: bytes,
    filename: str,
    vault_password: str,
    file_password: str | None
) -> bytes:
    """
    1. Apply file-level lock if supported (PDF)
    2. Apply vault encryption (AES-GCM)
    """

    # STEP 1: File-level protection (PDF only)
    if is_pdf(filename) and file_password:
        data = lock_pdf(data, file_password)

    # STEP 2: Vault encryption (ALL file types)
    return encrypt_bytes(data, vault_password)


# ===== STEP 7: DECRYPT PIPELINE =====
def process_and_decrypt(
    encrypted_data: bytes,
    vault_password: str
) -> bytes:
    """
    Decrypt vault-encrypted data.
    File-level protections (PDF password) remain intact.
    """
    return decrypt_bytes(encrypted_data, vault_password)
=======
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type

MAGIC = b"SFV1"
SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32  # AES-256


def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64 MB
        parallelism=2,
        hash_len=KEY_LEN,
        type=Type.ID,
    )


def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_LEN)
    nonce = os.urandom(NONCE_LEN)
    key = derive_key(password, salt)

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    return MAGIC + salt + nonce + ciphertext


def decrypt_bytes(blob: bytes, password: str) -> bytes:
    if len(blob) < len(MAGIC) + SALT_LEN + NONCE_LEN + 1:
        raise ValueError("Invalid encrypted file (too small).")

    if blob[:4] != MAGIC:
        raise ValueError("Invalid encrypted file (bad header).")

    salt = blob[4:4 + SALT_LEN]
    nonce = blob[4 + SALT_LEN:4 + SALT_LEN + NONCE_LEN]
    ciphertext = blob[4 + SALT_LEN + NONCE_LEN:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

from file_lockers import is_pdf, lock_pdf

def process_and_encrypt(
    data: bytes,
    filename: str,
    vault_password: str,
    file_password: str | None
) -> bytes:
    """
    1. Apply file-level lock if supported (PDF)
    2. Apply vault encryption (AES-GCM)
    """

    # STEP 1: File-level protection (PDF only)
    if is_pdf(filename) and file_password:
        data = lock_pdf(data, file_password)

    # STEP 2: Vault encryption (ALL file types)
    return encrypt_bytes(data, vault_password)


# ===== STEP 7: DECRYPT PIPELINE =====
def process_and_decrypt(
    encrypted_data: bytes,
    vault_password: str
) -> bytes:
    """
    Decrypt vault-encrypted data.
    File-level protections (PDF password) remain intact.
    """
    return decrypt_bytes(encrypted_data, vault_password)
>>>>>>> b0b3d9ab2bc4e15400b7ff27417f58933d8d9200
