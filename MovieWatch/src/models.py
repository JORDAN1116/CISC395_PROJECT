from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Movie:
    title: str
    genre: str
    rating: float
    watched: bool = False
    notes: str = ""
    image_url: str = ""
    id: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Watchlist:
    def __init__(self):
        self.movies: List[Movie] = []

    def add_movie(self, movie: Movie):
        self.movies.append(movie)

    def get_unwatched(self) -> List[Movie]:
        return [m for m in self.movies if not m.watched]

    def get_watched(self) -> List[Movie]:
        return [m for m in self.movies if m.watched]

    def get_top_rated(self, limit: int = 5) -> List[Movie]:
        return sorted(self.movies, key=lambda x: x.rating, reverse=True)[:limit]

    def find_by_title(self, title: str) -> Optional[Movie]:
        for m in self.movies:
            if m.title.lower() == title.lower():
                return m
        return None

    def clear(self):
        self.movies = []
