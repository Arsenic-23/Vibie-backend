const express = require('express');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const verifyTelegramAuth = require('../utils/verifyTelegramAuth');

const router = express.Router();

router.post('/telegram', async (req, res) => {
  const { authData } = req.body;

  if (!verifyTelegramAuth(authData)) {
    return res.status(401).json({ error: 'Invalid Telegram data' });
  }

  const { id, first_name, last_name, username, photo_url } = authData;

  let user = await User.findOne({ telegramId: id });

  if (!user) {
    user = await User.create({
      telegramId: id,
      first_name,
      last_name,
      username,
      photo_url,
    });
  }

  const token = jwt.sign({ id: user.telegramId }, process.env.JWT_SECRET, {
    expiresIn: '7d',
  });

  res.json({
    token,
    profile: {
      name: `${first_name || ''} ${last_name || ''}`.trim(),
      username,
      photo: photo_url,
    },
  });
});

module.exports = router;