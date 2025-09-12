import requests
from config import HEADERS

def find_movie_link(tmdb_id=None, imdb_id=None, title=None, is_tv=False, season=1, episode=1, full_season=False):
    """
    Get movie or TV embed link from 2Embed or Vidsrc.
    """
    embed_url = None

    # Choose correct ID priority
    if is_tv:
        content_id = tmdb_id or imdb_id or title   # TV shows → prefer TMDB
    else:
        content_id = imdb_id or tmdb_id or title   # Movies → prefer IMDb

    # --- 1. 2Embed ---
    try:
        if is_tv:
            if full_season:
                embed_url = f"https://www.2embed.cc/embedtvfull/{content_id}"
                print(f"📺 2Embed Full Season embed: {embed_url}")
            else:
                embed_url = f"https://www.2embed.cc/embedtv/{content_id}&s={season}&e={episode}"
                print(f"📺 2Embed TV Episode embed: {embed_url}")
        else:
            embed_url = f"https://www.2embed.cc/embed/{content_id}"
            print(f"🎬 2Embed Movie embed: {embed_url}")
    except Exception as e:
        print(f"❌ 2Embed error: {e}")

    # --- 2. Vidsrc fallback ---
    if not embed_url:
        try:
            if is_tv:
                if full_season:
                    embed_url = f"https://vidsrc.to/embed/tv/{content_id}/{season}"
                    print(f"📺 Vidsrc TV Season embed: {embed_url}")
                else:
                    embed_url = f"https://vidsrc.to/embed/tv/{content_id}/{season}/{episode}"
                    print(f"📺 Vidsrc TV Episode embed: {embed_url}")
            else:
                embed_url = f"https://vidsrc.to/embed/movie/{content_id}"
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
