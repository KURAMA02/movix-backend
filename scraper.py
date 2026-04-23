import requests
from config import HEADERS

# ========================
# Priority order:
# 1. Vidsrc (multi-domain)
# 2. 2embed.online (NEW)
# 3. FlixHQ (fallback)
# ========================

VIDSRC_DOMAINS = [
    "https://vidsrc-embed.ru",
    "https://vidsrc-embed.su",
    "https://vidsrcme.su",
    "https://vsrc.su"
]

def find_movie_link(tmdb_id=None, imdb_id=None, title=None, season=None, episode=None):
    embed_url = None

    # --- 1. Vidsrc ---
    try:
        for domain in VIDSRC_DOMAINS:
            if season and episode:
                test_url = f"{domain}/embed/tv?tmdb={tmdb_id}&season={season}&episode={episode}"
            else:
                if imdb_id:
                    test_url = f"{domain}/embed/movie?imdb={imdb_id}"
                else:
                    test_url = f"{domain}/embed/movie?tmdb={tmdb_id}"

            try:
                res = requests.get(test_url, headers=HEADERS, timeout=5)
                if res.status_code == 200:
                    embed_url = test_url
                    print(f"🎬 Vidsrc working: {embed_url}")
                    break
            except:
                continue

    except Exception as e:
        print(f"❌ Vidsrc error: {e}")


    # --- 2. 2Embed (UPDATED to 2embed.online) ---
    if not embed_url:
        try:
            if season and episode:
                # TV SHOW (NEW FORMAT)
                if imdb_id:
                    embed_url = f"https://www.2embed.online/embed/tv/{imdb_id}/{season}/{episode}"
                else:
                    embed_url = f"https://www.2embed.online/embed/tv/{tmdb_id}/{season}/{episode}"
                print(f"🎬 2Embed TV embed: {embed_url}")
            else:
                # MOVIE (NEW FORMAT)
                if imdb_id:
                    embed_url = f"https://www.2embed.online/embed/movie/{imdb_id}"
                else:
                    embed_url = f"https://www.2embed.online/embed/movie/{tmdb_id}"
                print(f"🎬 2Embed movie embed: {embed_url}")

        except Exception as e:
            print(f"❌ 2Embed error: {e}")


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
        return {"success": False, "message": "Movie not available"}

    return {
        "success": True,
        "server": "direct",
        "embed_url": embed_url
    }
