import json
import os
from .models import Movie, Watchlist

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "movies.json")

def save_watchlist(watchlist: Watchlist):
    """Saves the entire watchlist to a JSON file."""
    data = [movie.to_dict() for movie in watchlist.movies]
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_watchlist() -> Watchlist:
    """Loads the watchlist from a JSON file."""
    watchlist = Watchlist()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    watchlist.add_movie(Movie.from_dict(item))
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading watchlist: {e}")
    return watchlist
