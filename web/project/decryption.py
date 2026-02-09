import subprocess


def decrypt_secret(encrypted_string, key_string):
    """
    Takes the encrypted string and the key string and uses
    subprocess and openssl to decrypt the secret.
    """
    return subprocess.run(
        [
            "openssl", "enc", "-aes-256-cbc",
            "-pbkdf2", "-d", "-base64",
            "-pass", f"pass:{key_string}"
        ],
        input=f'{encrypted_string}\n',
        text=True,
        capture_output=True,
    ).stdout.strip()


def encrypt_secret(plain_text=None, encryption_key=None):
    """
    Takes the encrypted string and the key string and uses
    subprocess and openssl to decrypt the secret.
    """
    if not plain_text:
        plain_text = generate_secret()

    if not encryption_key:
        encryption_key = generate_secret()

    return subprocess.run(
        [
            "openssl", "enc", "-aes-256-cbc",
            "-pbkdf2", "-salt", "-base64",
            "-pass", f"pass:{encryption_key}"
        ],
        input=f'{plain_text}\n',
        text=True,
        capture_output=True,
    ).stdout.strip()


def generate_secret(length: int=32) -> str:
    """
    Uses subprocess and openssl to generate a secret.
    """
    return subprocess.run(
        ['openssl', 'rand', '-hex', str(length)],
        capture_output=True,
        text=True,
    ).stdout.strip()