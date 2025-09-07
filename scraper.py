import requests
from config import HEADERS

# ========================
# Priority order:
# 1. Vidsrc.to
# 2. 2embed.cc
# 3. FlixHQ (requires scraping fallback)
# ========================

def find_movie_link(tmdb_id=None, imdb_id=None, title=None):
    """ 
    Get movie embed link from Vidsrc, 2Embed, or FlixHQ. 
    Play immediately from direct source. Upload removed.
    """
    embed_url = None
    cache_key = tmdb_id or imdb_id or title

    # --- 1. Vidsrc.to ---
    try:
            if tmdb_id:
                embed_url = f"https://www.2embed.cc/embed/{tmdb_id}"
                print(f"🎬 2Embed embed: {embed_url}")
            elif imdb_id:
                embed_url = f"https://www.2embed.cc/embed/{imdb_id}"
                print(f"🎬 2Embed embed: {embed_url}")
    except Exception as e:
            print(f"❌ 2Embed error: {e}")
    

    # --- 2. 2embed.cc ---
    if not embed_url:
        try:
            if imdb_id:
                embed_url = f"https://vidsrc.to/embed/movie/{imdb_id}"
                print(f"🎬 Vidsrc.to embed: {embed_url}")
            elif tmdb_id:
                embed_url = f"https://vidsrc.to/embed/movie/{tmdb_id}"
            print(f"🎬 Vidsrc.to embed: {embed_url}")
        except Exception as e:
            print(f"❌ Vidsrc error: {e}")

    # --- 3. FlixHQ (scrape fallback) ---
    if not embed_url:
        try:
            search_url = f"https://flixhq.to/search/{tmdb_id or imdb_id}"
            print(f"🔍 FlixHQ search: {search_url}")
            res = requests.get(search_url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                embed_url = search_url  # just return search page for now
        except Exception as e:
            print(f"❌ FlixHQ error: {e}")

    if not embed_url:
        return {"success": False, "message": "Movie not available"}

    # return direct link immediately
    return {
        "success": True,
        "server": "direct",
        "embed_url": embed_url
    }
