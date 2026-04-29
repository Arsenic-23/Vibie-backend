<div align="center">
  <h1>🎧 Vibie Backend</h1>
  <p><strong>The powerhouse behind real-time social music streaming and group listening experiences.</strong></p>

  <!-- Badges -->
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
  <a href="https://www.mongodb.com/"><img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" /></a>
  <a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API"><img src="https://img.shields.io/badge/WebSockets-010101?style=for-the-badge&logo=socket.io&logoColor=white" alt="WebSockets" /></a>
</div>

## 📖 Overview

The **Vibie Backend** is a high-performance REST API and WebSocket server built with **FastAPI**. It serves as the core infrastructure for the Vibie platform, enabling users to listen to music together in real-time. By leveraging asynchronous Python and WebSockets, it ensures perfectly synced playback across all clients in a group session.

## ✨ Key Features

- **🚀 High Performance**: Built on FastAPI and Uvicorn for incredibly fast asynchronous request handling.
- **🎧 Real-Time Group Streaming**: WebSockets sync music playback, queues, and chat states instantly among group members.
- **🔍 Advanced Music Search**: Search and stream audio seamlessly (powered by `yt-dlp`).
- **🗄️ Scalable Data Storage**: Uses **MongoDB** (via Motor) for efficient, asynchronous database operations.
- **🔐 Secure Authentication**: Robust security implemented with JWT, Bcrypt, and PyJOSE.
- **🎶 Explore & Genres**: Endpoints dedicated to music discovery, genre browsing, and curated playlists.

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Language**: Python 3.9+
- **Database**: MongoDB (Motor / PyMongo)
- **Real-Time Communication**: WebSockets, `python-socketio`
- **Audio Processing / Integration**: `yt-dlp`, Google API Client
- **Authentication**: `passlib`, `bcrypt`, `python-jose`, `PyJWT`
- **Deployment Ready**: Fully configured for [Render](https://render.com/) deployment (`render.yaml` included).

---

## 🚀 Getting Started

Follow these steps to run the backend locally.

### Prerequisites

- **Python 3.9+** installed on your local machine.
- **MongoDB** instance (local or Atlas) running.
- **FFmpeg** (optional, depending on your yt-dlp streaming requirements).

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Vibie-backend.git
cd Vibie-backend
```

### 2. Set up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory and add the necessary variables:

```env
PORT=10000
BACKEND_URL=http://localhost:10000
MONGO_URI=your_mongodb_connection_string
DB_NAME=vibie_db
JWT_SECRET=your_super_secret_jwt_key
BOT_TOKEN=your_telegram_or_discord_bot_token_if_applicable
```

### 5. Run the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
```

The API will be available at `http://localhost:10000`.

---

## 📚 API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access:

- **Swagger UI**: `http://localhost:10000/docs`
- **ReDoc**: `http://localhost:10000/redoc`

### Core Endpoints

- `GET /health` - Health check status.
- `GET /api/search/` - Search for tracks.
- `GET /api/explore/` - Discover trending or new tracks.
- `GET /api/genres/` - Retrieve available music genres.
- `POST /api/stream/group/{chat_id}/play` - Add a song to a group's queue.
- `WS /ws/stream/{stream_id}` - WebSocket connection for real-time stream state.

---

## ☁️ Deployment

This project includes a `render.yaml` file for frictionless deployment on **Render**.

1. Connect your GitHub repository to Render.
2. Render will automatically detect the `render.yaml` file as a Blueprint.
3. Add your environment variables (`MONGO_URI`, `JWT_SECRET`, etc.) in the Render dashboard.
4. Deploy!

---

## 🤝 Contributing

Contributions are always welcome! Feel free to open an issue or submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
