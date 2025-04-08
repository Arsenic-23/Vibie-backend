import hashlib
import hmac
import time
from urllib.parse import parse_qsl
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def verify_telegram_auth(init_data: str):
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
        hash_value = parsed_data.pop("hash", None)
        auth_date = int(parsed_data.get("auth_date", "0"))

        # Optional: block old logins
        if time.time() - auth_date > 86400:
            return None

        data_check_string = "\n".join(
            [f"{k}={v}" for k, v in sorted(parsed_data.items())]
        )

        secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
        computed_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        if computed_hash != hash_value:
            return None

        return parsed_data
    except Exception as e:
        print(f"Auth error: {e}")
        return None