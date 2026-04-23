# api.py
from flask import Flask, request, jsonify
from scraper import find_movie_link
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/find_movie", methods=["GET"])
def find_movie():
    tmdb_id = request.args.get("tmdb_id")
    imdb_id = request.args.get("imdb_id")
    title = request.args.get("title")

    result = find_movie_link(tmdb_id=tmdb_id, imdb_id=imdb_id, title=title)

    if result:
        return jsonify(result)

    return jsonify({"success": False, "message": "Movie not found on sources"})


# =========================
# ✅ UPDATED TV ENDPOINT (supports Vidsrc + 2Embed.online)
# =========================
@app.route("/find_tv", methods=["GET"])
def find_tv():
    tmdb_id = request.args.get("tmdb_id")
    season = request.args.get("season")
    episode = request.args.get("episode")

    embed_url = None

    # --- 1. Try Vidsrc domains first ---
    vidsrc_domains = [
        "https://vidsrc-embed.ru",
        "https://vidsrc-embed.su",
        "https://vidsrcme.su",
        "https://vsrc.su"
    ]

    for domain in vidsrc_domains:
        embed_url = f"{domain}/embed/tv?tmdb={tmdb_id}&season={season}&episode={episode}"
        break  # keep same logic (no validation added)

    # --- 2. Fallback to 2Embed.online (NEW) ---
    if not embed_url:
        try:
            embed_url = f"https://www.2embed.online/embed/tv/{tmdb_id}/{season}/{episode}"
        except:
            pass

    if not embed_url:
        return jsonify({"success": False, "message": "TV episode not available"})

    return jsonify({
        "success": True,
        "server": "direct",
        "embed_url": embed_url
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
