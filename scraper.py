import requests
from config import HEADERS

# ========================
# Priority order:
# 1. VidFast
# 2. VidLink
# 3. Vidsrc
# 4. 2Embed
# 5. FlixHQ
# ========================

VIDSRC_DOMAINS = [
    "https://vidsrc.to",
    "https://vidsrc.sbs"
]

def find_movie_link(tmdb_id=None, imdb_id=None, title=None, season=None, episode=None):

    embed_url = None
    servers = []


    # ==========================================
    # 1. VIDfast (NEW PRIMARY)
    # ==========================================
    try:
        if tmdb_id or imdb_id:

            media_id = imdb_id if imdb_id else tmdb_id

            if season and episode:
                url = (
                    f"https://vidfast.pro/tv/"
                    f"{media_id}/{season}/{episode}"
                    "?autoPlay=true"
                )
                print(f"🎬 VidFast TV: {url}")

            else:
                url = (
                    f"https://vidfast.io/movie/"
                    f"{media_id}"
                    "?autoPlay=true"
                )
                print(f"🎬 VidFast Movie: {url}")

            servers.append({
                "name": "VidFast",
                "url": url
            })
          
            embed_url = url

    except Exception as e:
        print(f"❌ VidFast error: {e}")

    # ==========================================
    # 2. VIDLINK
    # ==========================================
    try:
        if tmdb_id:
            if season and episode:
                url = f"https://vidlink.pro/tv/{tmdb_id}/{season}/{episode}"
                print(f"🎬 VidLink TV: {url}")
            else:
                url = f"https://vidlink.pro/movie/{tmdb_id}"
                print(f"🎬 VidLink Movie: {url}")

            servers.append({
                "name": "VidLink",
                "url": url
            })
            if not embed_url:
                embed_url = url

    except Exception as e:
        print(f"❌ VidLink error: {e}")

    # ==========================================
    # 3. 111Movies
    # ==========================================
    try:
        if tmdb_id or imdb_id:

            media_id = imdb_id if imdb_id else tmdb_id

            if season and episode:
                url = (
                    f"https://111movies.net/tv/"
                    f"{media_id}/{season}/{episode}"
                    "?autoPlay=true"
                )
                print(f"🎬 111movies.net TV: {url}")

            else:
                url = (
                    f"https://111movies.net/movie/"
                    f"{media_id}"
                    "?autoPlay=true"
                )
                print(f"🎬 111movies.net: {url}")

            servers.append({
                "name": "111movies",
                "url": url
            })
          
            embed_url = url

    except Exception as e:
        print(f"❌ 111movies: {e}")


    # ==========================================
    # 4. Vidsrc
    # ==========================================
    try:
        if tmdb_id or imdb_id:

            media_id = imdb_id if imdb_id else tmdb_id

            if season and episode:
                url = (
                    f"https://vidsrc.sbs/tv/"
                    f"{media_id}/{season}/{episode}"
                    "?autoPlay=true"
                )
                print(f"🎬 vidsrc TV: {url}")

            else:
                url = (
                    f"https://vidsrc.sbs/movie/"
                    f"{media_id}"
                    "?autoPlay=true"
                )
                print(f"🎬 vidsrc: {url}")

            servers.append({
                "name": "vidsrc.sbs",
                "url": url
            })
          
            embed_url = url

    except Exception as e:
        print(f"❌ vidsrc: {e}")


    # ==========================================
    # 5. 2Embed
    # ==========================================
    try:
        if season and episode:
            if imdb_id:
                url = f"https://www.2embed.cc/embed/tv/{imdb_id}/{season}/{episode}"
            else:
                url = f"https://www.2embed.cc/embed/tv/{tmdb_id}/{season}/{episode}"

            print(f"🎬 2Embed TV embed: {url}")

        else:
            if imdb_id:
                url = f"https://www.2embed.cc/embed/movie/{imdb_id}"
            else:
                url = f"https://www.2embed.cc/embed/movie/{tmdb_id}"

            print(f"🎬 2Embed movie embed: {url}")

        servers.append({
            "name": "2Embed",
            "url": url
        })

    except Exception as e:
        print(f"❌ 2Embed error: {e}")


    # ==========================================
    # 6. FlixHQ fallback
    # ==========================================
    try:
        search_url = f"https://flixhq.to/search/{tmdb_id or imdb_id}"
        print(f"🔍 FlixHQ search: {search_url}")

        servers.append({
            "name": "FlixHQ",
            "url": search_url
        })

        if not embed_url:
            embed_url = search_url

    except Exception as e:
        print(f"❌ FlixHQ error: {e}")


    # ==========================================
    # FINAL CHECK
    # ==========================================
    if not servers:
        return {"success": False, "message": "Movie not available"}

    return {
        "success": True,
        "server": "VidFast",
        "servers": servers
    }
