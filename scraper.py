import requests
from config import HEADERS, API_KEY

def get_imdb_from_tmdb(tmdb_id, is_tv=False):
    """Fetch IMDb ID from TMDB (works for movies + tv)."""
    try:
        if is_tv:
            url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/external_ids?api_key={API_KEY}"
        else:
            url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={API_KEY}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.json().get("imdb_id")
    except Exception as e:
        print(f"❌ Failed to fetch IMDb ID: {e}")
    return None


def find_movie_link(tmdb_id=None, imdb_id=None, title=None, is_tv=False):
    """Get movie or TV embed link from Vidsrc, 2Embed, or FlixHQ."""
    embed_url = None

    # Resolve IMDb if only TMDB is given
    if not imdb_id and tmdb_id:
        imdb_id = get_imdb_from_tmdb(tmdb_id, is_tv=is_tv)

    # --- 1. 2Embed ---
    try:
        if is_tv:
            if imdb_id:
                embed_url = f"https://www.2embed.cc/embedtv/{imdb_id}"
                print(f"📺 2Embed TV embed: {embed_url}")
        else:
            if tmdb_id:
                embed_url = f"https://www.2embed.cc/embed/{tmdb_id}"
                print(f"🎬 2Embed movie embed: {embed_url}")
    except Exception as e:
        print(f"❌ 2Embed error: {e}")

    # --- 2. Vidsrc.to ---
    if not embed_url:
        try:
            if is_tv:
                if imdb_id:
                    embed_url = f"https://vidsrc.to/embed/tv/{imdb_id}"
                    print(f"📺 Vidsrc TV embed: {embed_url}")
            else:
                if imdb_id:
                    embed_url = f"https://vidsrc.to/embed/movie/{imdb_id}"
                    print(f"🎬 Vidsrc movie embed: {embed_url}")
        except Exception as e:
            print(f"❌ Vidsrc error: {e}")

    # --- 3. FlixHQ fallback ---
    if not embed_url:
        try:
            search_url = f"https://flixhq.to/search/{tmdb_id or imdb_id}"
            print(f"🔍 FlixHQ search: {search_url}")
            res = requests.get(search_url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                embed_url = search_url
        except Exception as e:
            print(f"❌ FlixHQ error: {e}")

    if not embed_url:
        return {"success": False, "message": "Content not available"}

    return {
        "success": True,
        "server": "direct",
        "embed_url": embed_url
    }
