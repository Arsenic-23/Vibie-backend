# app/utils/verify_telegram_auth.py

import hashlib
import hmac
import os


def verify_telegram_auth(auth_data: dict) -> bool:
    """
    Verifies Telegram authentication payload using the Telegram login protocol.
    """

    try:
        auth_data = dict(auth_data)
        received_hash = auth_data.pop("hash", None)

        if not received_hash:
            return False

        # Create the data check string
        data_check_string = "\n".join(
            f"{k}={auth_data[k]}" for k in sorted(auth_data)
        )

        # Get the Telegram bot token
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            raise RuntimeError("BOT_TOKEN environment variable is missing.")

        # Calculate HMAC-SHA256 hash
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        return hmac.compare_digest(calculated_hash, received_hash)

    except Exception as e:
        print("Telegram auth verification error:", e)
        return False