import sys
import os

# Fix the import path so it works when run from the MovieWatch/ root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import Movie, Watchlist
from src.storage import load_watchlist, save_watchlist

def main():
    collection = load_watchlist()

    while True:
        print("\n=== Movie Watch ===")
        print("[1] Add movie")
        print("[2] View all unwatched")
        print("[3] Search by rating")
        print("[4] Random pick from list")
        print("[5] Quit")

        choice = input("Select an option: ")

        if choice == '1':
            title = input("Movie Title: ")
            genre = input("Genre: ")
            try:
                rating = float(input("Rating: "))
            except ValueError:
                print("Invalid rating. Please enter a number.")
                continue
            
            new_movie = Movie(title=title, genre=genre, rating=rating)
            collection.add_movie(new_movie)
            save_watchlist(collection)
            print(f"Added {title}!")

        elif choice == '2':
            unwatched = collection.get_unwatched()
            if not unwatched:
                print("No movie in list.")
            else:
                for i, m in enumerate(unwatched, 1):
                    print(f"{i}. {m.title} ({m.genre}) - ⭐{m.rating}")

        elif choice == '3':
            try:
                min_rating = float(input("Enter minimum rating: "))
            except ValueError:
                print("Invalid rating. Please enter a number.")
                continue
            
            results = collection.search_by_rating(min_rating)
            if not results:
                print("No movies found with that rating.")
            else:
                for i, m in enumerate(results, 1):
                    print(f"{i}. {m.title} ({m.genre}) - ⭐{m.rating}")

        elif choice == '4':
            movie = collection.random_pick()
            if movie:
                print(f"Random Pick: {movie.title} ({movie.genre}) - ⭐{movie.rating}")
            else:
                print("Your list is empty.")

        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
