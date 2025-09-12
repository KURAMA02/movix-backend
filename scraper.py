import requests
from config import HEADERS

def find_movie_link(tmdb_id=None, imdb_id=None, title=None, is_tv=False, season=1, episode=1, full_season=False):
    """
    Get movie or TV embed link from 2Embed or Vidsrc.
    """
    embed_url = None
    cache_key = tmdb_id or imdb_id or title

    # --- 1. 2Embed ---
    try:
        if is_tv:
            if full_season:
                if tmdb_id:
                    embed_url = f"https://www.2embed.cc/embedtvfull/{tmdb_id}"
                elif imdb_id:
                    embed_url = f"https://www.2embed.cc/embedtvfull/{imdb_id}"
                print(f"📺 2Embed Full Season embed: {embed_url}")
            else:
                if tmdb_id:
                    embed_url = f"https://www.2embed.cc/embedtv/{tmdb_id}&s={season}&e={episode}"
                elif imdb_id:
                    embed_url = f"https://www.2embed.cc/embedtv/{imdb_id}&s={season}&e={episode}"
                print(f"📺 2Embed TV Episode embed: {embed_url}")
        else:
            if tmdb_id:
                embed_url = f"https://www.2embed.cc/embed/{tmdb_id}"
            elif imdb_id:
                embed_url = f"https://www.2embed.cc/embed/{imdb_id}"
            print(f"🎬 2Embed Movie embed: {embed_url}")
    except Exception as e:
        print(f"❌ 2Embed error: {e}")

    # --- 2. Vidsrc fallback ---
    if not embed_url:
        try:
            if is_tv:
                if tmdb_id:
                    embed_url = f"https://vidsrc.to/embed/tv/{tmdb_id}"
                elif imdb_id:
                    embed_url = f"https://vidsrc.to/embed/tv/{imdb_id}"
                print(f"📺 Vidsrc TV embed: {embed_url}")
            else:
                if tmdb_id:
                    embed_url = f"https://vidsrc.to/embed/movie/{tmdb_id}"
                elif imdb_id:
                    embed_url = f"https://vidsrc.to/embed/movie/{imdb_id}"
                print(f"🎬 Vidsrc Movie embed: {embed_url}")
        except Exception as e:
            print(f"❌ Vidsrc error: {e}")

    # --- No sources found ---
    if not embed_url:
        return {"success": False, "message": "Content not available"}

    return {
        "success": True,
        "server": "direct",
        "embed_url": embed_url
    }
