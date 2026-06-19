import requests
from config import HEADERS

# ========================
# Priority order:
# 1. VidLink (NEW PRIMARY)
# 2. Vidsrc
# 3. 2Embed
# 4. FlixHQ
# ========================

VIDSRC_DOMAINS = [
    "https://vidsrc-embed.ru",
    "https://vidsrc-embed.su",
    "https://vidsrcme.su",
    "https://vsrc.su"
]

def find_movie_link(tmdb_id=None, imdb_id=None, title=None, season=None, episode=None):

    embed_url = None
    servers = []

    # ==========================================
    # 1. VIDLINK (NEW PRIMARY)
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

            embed_url = url

    except Exception as e:
        print(f"❌ VidLink error: {e}")


    # ==========================================
    # 2. Vidsrc
    # ==========================================
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
                    print(f"🎬 Vidsrc working: {test_url}")

                    servers.append({
                        "name": f"Vidsrc ({domain.replace('https://','')})",
                        "url": test_url
                    })

                    break
            except:
                continue

    except Exception as e:
        print(f"❌ Vidsrc error: {e}")


    # ==========================================
    # 3. 2Embed
    # ==========================================
    try:
        if season and episode:
            if imdb_id:
                url = f"https://www.2embed.online/embed/tv/{imdb_id}/{season}/{episode}"
            else:
                url = f"https://www.2embed.online/embed/tv/{tmdb_id}/{season}/{episode}"

            print(f"🎬 2Embed TV embed: {url}")

        else:
            if imdb_id:
                url = f"https://www.2embed.online/embed/movie/{imdb_id}"
            else:
                url = f"https://www.2embed.online/embed/movie/{tmdb_id}"

            print(f"🎬 2Embed movie embed: {url}")

        servers.append({
            "name": "2Embed",
            "url": url
        })

    except Exception as e:
        print(f"❌ 2Embed error: {e}")


    # ==========================================
    # 4. FlixHQ fallback
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
        "server": "VidLink",
        "servers": servers
    }
