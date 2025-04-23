# app/services/genre_service.py

from app.db.mock_db import get_all_songs

def get_all_genres():
    all_songs = get_all_songs()
    genres = set(song["genre"] for song in all_songs)
    return sorted(list(genres))


def get_genre_data(genre_name: str):
    all_songs = get_all_songs()
    genre_songs = [s for s in all_songs if s["genre"].lower() == genre_name.lower()]

    top_songs = sorted(genre_songs, key=lambda s: s.get("popularity", 0), reverse=True)[:10]
    new_releases = sorted(genre_songs, key=lambda s: s.get("release_date", "2000-01-01"), reverse=True)[:10]
    most_played = sorted(genre_songs, key=lambda s: s.get("play_count", 0), reverse=True)[:10]

    return {
        "genre": genre_name.title(),
        "top_songs": top_songs,
        "new_releases": new_releases,
        "most_played": most_played
    }