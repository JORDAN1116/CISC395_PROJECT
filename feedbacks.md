# MovieWatch Project - Feedback & Recommendations

Here are some simple, easy, and actionable recommendations to improve your draft project:

### 1. Automate Unique ID Generation (Cleaner Code)
In `src/models.py`, the `Movie` dataclass expects the `id` to be instantiated manually. This leads to awkward code in `app.py` where you have to check `if m.id is None:` and do an inline `import uuid`. 

**Fix:** Auto-generate the ID when the object is created using `field(default_factory=...)`.
```python
# In src/models.py
import uuid
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Movie:
    title: str
    genre: str
    rating: float
    watched: bool = False
    notes: str = ""
    image_url: str = ""
    # Auto-generate UUID by default
    id: str = field(default_factory=lambda: str(uuid.uuid4())) 
```
*This allows you to remove all the manual `uuid` imports and assignment logic from `app.py`.*

### 2. Make AI Parsing More Robust
In `app.py`, the code splits the AI's response using `genre, rating = details.split("|")`. This is very fragile; Large Language Models often output conversational filler (e.g., *"Here is your result: Action | 8.5"*), which will instantly crash your app.

**Fix:** Instruct the AI to return JSON and parse it using Python’s `json` module.
```python
import json

# Update prompt
prompt = f"Return ONLY valid JSON for the movie '{new_title}'. Format: {{\\"genre\\": \\"...\\", \\"rating\\": 8.5}}"
details = ask_ai(prompt)

try:
    data = json.loads(details)
    genre = data.get("genre", "Unknown")
    rating = float(data.get("rating", 5.0))
except json.JSONDecodeError:
    genre, rating = "Unknown", 5.0
```

### 3. Check the DuckDuckGo Import
In `src/search_tools.py`, you are using `from ddgs import DDGS`. 
If you are using the standard community package, the correct import is almost always:
```python
from duckduckgo_search import DDGS
```
Ensure you run `pip install duckduckgo-search` and fix that import if you are getting `ModuleNotFoundError` locally.

### 4. Create a Project-Specific `requirements.txt`
Right now, the `requirements.txt` in the parent folder includes a lot of unrelated items. The `MovieWatch/` folder should have its own neat `requirements.txt` containing only what this specific app needs:
```text
streamlit
openai
python-dotenv
chromadb
sentence-transformers
duckduckgo-search
```

### 5. Encapsulate RAG + Watchlist Saving
In `app.py`, every time a movie is added or edited, you manually do `st.session_state.watchlist.add(...)`, update RAG, and then call `persist()`.

**Fix:** It’s much cleaner to add an `add_movie` and `update_notes` method inside your `Watchlist` class (or a dedicated manager) within `src/storage.py` that handles the database update, the JSON save, and the RAG indexing all in one place so the Streamlit UI code stays minimal.
