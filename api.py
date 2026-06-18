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
# TV ENDPOINT (UPDATED MINIMALLY)
# =========================
@app.route("/find_tv", methods=["GET"])
def find_tv():
    tmdb_id = request.args.get("tmdb_id")
    season = request.args.get("season")
    episode = request.args.get("episode")

    # ✅ ONLY CHANGE: use scraper (same as movies)
    result = find_movie_link(
        tmdb_id=tmdb_id,
        season=season,
        episode=episode
    )

    if result:
        return jsonify(result)

    return jsonify({"success": False, "message": "TV episode not available"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
