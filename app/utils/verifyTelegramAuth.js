const crypto = require('crypto');

function verifyTelegramAuth(data) {
  const { hash, ...fields } = data;
  const sorted = Object.keys(fields)
    .sort()
    .map(key => `${key}=${fields[key]}`)
    .join('\n');

  const secret = crypto.createHash('sha256').update(process.env.TELEGRAM_BOT_TOKEN).digest();
  const hmac = crypto.createHmac('sha256', secret).update(sorted).digest('hex');

  return hmac === hash;
}

module.exports = verifyTelegramAuth;