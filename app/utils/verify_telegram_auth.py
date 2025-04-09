# app/utils/verify_telegram_auth.py

import hashlib
import hmac
import os
from urllib.parse import unquote

def verify_telegram_auth(auth_data: dict) -> bool:
    auth_data = {k: v for k, v in auth_data.items()}
    received_hash = auth_data.pop("hash", None)
    
    data_check_string = "\n".join(
        f"{k}={auth_data[k]}" for k in sorted(auth_data)
    )
    
    secret_key = hashlib.sha256(os.getenv("BOT_TOKEN", "").encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(calculated_hash, received_hash)