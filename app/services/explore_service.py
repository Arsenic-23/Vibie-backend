# app/services/explore_service.py

import random
from datetime import datetime
from app.db.mock_db import get_all_songs  # This can later be replaced by real DB calls

def get_explore_data():
    all_songs = get_all_songs()

    # Random shuffling to simulate trending and new releases
    trending = sorted(all_songs, key=lambda x: x.get("popularity", 0), reverse=True)[:15]
    new_releases = sorted(all_songs, key=lambda x: x.get("release_date", "2000-01-01"), reverse=True)[:15]
    top_charts = sorted(all_songs, key=lambda x: x.get("play_count", 0), reverse=True)[:15]

    return {
        "date": datetime.utcnow().isoformat(),
        "trending": trending,
        "new_releases": new_releases,
        "top_charts": top_charts
    }