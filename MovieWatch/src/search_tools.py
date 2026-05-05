from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 3) -> str:
    """Performs a web search for movie info."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No information found."
        
        formatted_results = []
        for r in results:
            formatted_results.append(f"{r['title']}\\n{r['body']}\\nLink: {r['href']}")
        
        return "\\n\\n".join(formatted_results)

def image_search(query: str) -> str:
    """Searches for a movie poster image URL."""
    try:
        with DDGS() as ddgs:
            # Adding 'movie poster' to the query to get better results
            results = list(ddgs.images(f"{query} movie poster", max_results=1))
            if results:
                return results[0]['image']
    except Exception as e:
        print(f"Image search error: {e}")
    
    # Return a default placeholder if search fails
    return "https://via.placeholder.com/300x450?text=No+Poster+Found"
