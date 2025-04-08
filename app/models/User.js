const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  telegramId: { type: String, required: true, unique: true },
  first_name: String,
  last_name: String,
  username: String,
  photo_url: String,
});

module.exports = mongoose.model('User', userSchema);