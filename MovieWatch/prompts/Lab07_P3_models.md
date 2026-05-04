I am building a Movie watchlist app. The project structure is: 

MovieWatch/
  ├── src/models.py    ← this file to create
  ├── src/storage.py   (coming later)
  ├── src/main.py      (coming later)
  └── data/

  Create src/models.py with TWO classes using only the Python standard library
(dataclasses, datetime). No pip installs needed.

Class 1: Movie (@dataclass)
- title: str             (Movie title, e.g. "Jaws")
- genre: str             (genre type)
- rating: float          (general movie rating)

Class 2: Watchlist 
- stores a list of Movie objects
- Methods:
  - unwatchedlist - add Movies that haven't been wathced to a list
  - top-rated - get Movies that were rated highly from list
  - Random pick - randomly pick a movie from list

Do not add an if __name__ == "__main__" block.
Write the file directly to src/models.py.