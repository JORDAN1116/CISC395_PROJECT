import streamlit as st
import uuid
from src.models import Movie, Watchlist
from src.storage import load_watchlist, save_watchlist
from src.ai_assistant import ask_ai, MOVIE_SYSTEM_PROMPT
from src.search_tools import web_search, image_search
from src.rag_engine import get_rag_engine

# --- Configuration & State ---
st.set_page_config(page_title="MovieWatch AI", page_icon="🎬", layout="wide")

if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist()

if "rag" not in st.session_state:
    st.session_state.rag = get_rag_engine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def persist():
    save_watchlist(st.session_state.watchlist)

# --- Sidebar: My Watchlist ---
st.sidebar.title("🎬 MovieWatch AI")
st.sidebar.markdown("---")

# Add Movie Form
with st.sidebar.expander("➕ Add New Movie", expanded=False):
    new_title = st.text_input("Movie Title")
    if st.button("Auto-Fetch & Add"):
        if new_title:
            with st.spinner(f"Fetching details for {new_title}..."):
                # Get Image
                poster_url = image_search(new_title)
                # Get AI Details (Genre and simplified Rating)
                details = ask_ai(f"Return ONLY the genre and a numeric rating (0-10) for the movie '{new_title}'. Format: Genre | Rating")
                try:
                    genre, rating = details.split("|")
                    rating = float(rating.strip())
                except:
                    genre, rating = "Unknown", 5.0
                
                # Get AI Summary for Notes
                summary = ask_ai(f"Provide a 2-sentence summary of the movie '{new_title}'.")
                
                new_movie = Movie(
                    title=new_title,
                    genre=genre.strip(),
                    rating=rating,
                    image_url=poster_url,
                    notes=summary,
                    id=str(uuid.uuid4())
                )
                st.session_state.watchlist.add_movie(new_movie)
                # Index in RAG
                st.session_state.rag.index_movie(new_movie.id, summary, {"title": new_title})
                persist()
                st.success(f"Added {new_title}!")
                st.rerun()

st.sidebar.subheader("🍿 Unwatched")
unwatched = st.session_state.watchlist.get_unwatched()

if not unwatched:
    st.sidebar.info("Your watchlist is empty. Add a movie to start!")
else:
    for idx, m in enumerate(unwatched):
        with st.sidebar.container(border=True):
            cols = st.columns([1, 2])
            with cols[0]:
                if m.image_url:
                    st.image(m.image_url, use_container_width=True)
                else:
                    st.write("No Image")
            with cols[1]:
                st.markdown(f"**{m.title}**")
                st.caption(f"{m.genre} • ⭐{m.rating}")
                if st.button("Done", key=f"watch_{m.id}_{idx}"):
                    m.watched = True
                    persist()
                    st.rerun()
            with st.expander("📝 Edit Notes", expanded=False):
                new_note = st.text_area("Your Thoughts", value=m.notes, height=100, key=f"ta_{m.id}_{idx}", label_visibility="collapsed")
                if st.button("Save", key=f"save_{m.id}_{idx}", use_container_width=True):
                    m.notes = new_note
                    if m.id is None:
                        import uuid
                        m.id = str(uuid.uuid4())
                    st.session_state.rag.index_movie(m.id, new_note, {"title": m.title})
                    persist()
                    st.rerun()

# --- Main Area ---
tab1, tab2, tab3 = st.tabs(["💬 Cinephile Chat", "🔍 Discovery", "🧠 Search My Thoughts"])

with tab1:
    st.subheader("Talk to Cinephile AI")
    st.caption("Ask for recommendations, trivia, or details about your list.")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("What should I watch tonight?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Contextualize with watchlist
            context = "My current unwatched movies are: " + ", ".join([m.title for m in unwatched])
            full_prompt = f"""{context}

User Question: {prompt}"""
            response = ask_ai(full_prompt)
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})

with tab2:
    st.subheader("Global Movie Discovery")
    search_q = st.text_input("Search the web for movies, actors, or trends...")
    if search_q:
        with st.spinner("Searching..."):
            results = web_search(search_q)
            st.markdown(results)

with tab3:
    st.subheader("Semantic Note Search")
    st.caption("Search through your personal movie notes using AI meanings.")
    rag_q = st.text_input("e.g., 'Movies with great visuals' or 'Depressing endings'")
    if rag_q:
        results = st.session_state.rag.search_notes(rag_q)
        if results and results['documents']:
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                with st.expander(f"Result: {meta['title']}"):
                    st.write(doc)
        else:
            st.write("No matching notes found.")
