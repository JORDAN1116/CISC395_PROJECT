I am building a Movie watchlist app.

The project already has:
- src/models.py with Movie (@dataclass) and Watchlist
  Watchlist methods: 
  - unwatchedlist - add Movies that haven't been wathced to a list
  - top-rated - get Movies that were rated highly from list
  - Random pick - randomly pick a movie from list

Read src/models.py first, then create src/main.py.

src/main.py must:
1. Fix the import path at the top so it works when run from the MovieWatch/ root:
       import sys, os
       sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

2. Import Movie, Watchlist from src.models
   

3. Show this menu in a loop until the user quits:
       === Movie Watch ===
       [1] Add movie
       [2] View all unwatched
       [3] Search by rating
       [4] Random pick from list
       [5] Quit

5. Implement each option using Watchlist methods:
   [1] Add: input title, genre, rating (float) -> Movie -> collection.add() -> save_movie()
   [2] View all: if len(collection) == 0 print "No movie in list."
       else print each Movie numbered with title, genre, rating
   [3] Search: input rating -> collection.search_by_rating() -> print results
   [4] Random Pick: randomly select Movie from collection -> print result
   [5] Quit: print "Goodbye!" and exit

6. Handle invalid menu input with: print("Invalid option, try again.")

Use only input() and print(). No external libraries.
Write the file directly to src/main.py.
