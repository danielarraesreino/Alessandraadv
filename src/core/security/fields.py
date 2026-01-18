from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class EncryptedField(models.CharField):
    """
    Saves encrypted data to the DB and decrypts it when reading.
    Requires settings.ENCRYPTION_KEY (32 url-safe base64-encoded bytes).
    """

    def __init__(self, *args, **kwargs):
        if not hasattr(settings, 'ENCRYPTION_KEY'):
            # Generate a key if not present (for dev/test simplicity, though ideally should be from env)
            settings.ENCRYPTION_KEY = Fernet.generate_key()
        self.fernet = Fernet(settings.ENCRYPTION_KEY)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            return self.fernet.decrypt(value.encode()).decode()
        except Exception:
            # If decryption fails (e.g. key changed), return raw or handle error
            return value

    def to_python(self, value):
        if value is None:
            return value
        # If it's already decrypted (normal string usage)
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        # Encrypt before saving
        return self.fernet.encrypt(value.encode()).decode()
