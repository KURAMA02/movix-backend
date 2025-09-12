import requests
from config import HEADERS

def find_movie_link(tmdb_id=None, imdb_id=None, title=None, is_tv=False):
    """ 
    Get movie or TV embed link from Vidsrc, 2Embed, or FlixHQ. 
    """
    embed_url = None
    cache_key = tmdb_id or imdb_id or title

    # --- 1. 2Embed ---
    try:
        if is_tv:
            if tmdb_id:
                embed_url = f"https://www.2embed.cc/embedtv/{tmdb_id}"
                print(f"📺 2Embed TV embed: {embed_url}")
            elif imdb_id:
                embed_url = f"https://www.2embed.cc/embedtv/{imdb_id}"
                print(f"📺 2Embed TV embed: {embed_url}")
        else:
            if tmdb_id:
                embed_url = f"https://www.2embed.cc/embed/{tmdb_id}"
                print(f"🎬 2Embed movie embed: {embed_url}")
            elif imdb_id:
                embed_url = f"https://www.2embed.cc/embed/{imdb_id}"
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
                elif tmdb_id:
                    embed_url = f"https://vidsrc.to/embed/tv/{tmdb_id}"
                    print(f"📺 Vidsrc TV embed: {embed_url}")
            else:
                if imdb_id:
                    embed_url = f"https://vidsrc.to/embed/movie/{imdb_id}"
                    print(f"🎬 Vidsrc movie embed: {embed_url}")
                elif tmdb_id:
                    embed_url = f"https://vidsrc.to/embed/movie/{tmdb_id}"
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
