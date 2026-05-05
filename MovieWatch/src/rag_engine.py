import chromadb
from sentence_transformers import SentenceTransformer
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "movie_notes"

class RAGEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def index_movie(self, movie_id: str, notes: str, metadata: dict):
        """Indexes or updates a movie's notes in the vector DB."""
        if not notes.strip():
            return
        
        embedding = self.model.encode(notes).tolist()
        
        self.collection.upsert(
            ids=[movie_id],
            embeddings=[embedding],
            documents=[notes],
            metadatas=[metadata]
        )

    def search_notes(self, query: str, n_results: int = 3):
        """Searches movie notes semantically."""
        if self.collection.count() == 0:
            return {"documents": [], "metadatas": []}
            
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results

def get_rag_engine():
    return RAGEngine()
