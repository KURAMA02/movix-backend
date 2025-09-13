from flask import Flask, request, jsonify
from scraper import find_movie_link
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "Backend is running!"})

@app.route("/find_movie", methods=["GET"])
def find_movie():
    tmdb_id = request.args.get("tmdb_id")
    imdb_id = request.args.get("imdb_id")
    title = request.args.get("title")
    content_type = request.args.get("type", "movie")  # default = movie
    is_tv = content_type.lower() == "tv"

    # ✅ NEW: handle season/episode/full_season params
    season_param = request.args.get("season")
    episode_param = request.args.get("episode")
    full_season_param = request.args.get("full_season", "false").lower()

    try:
        season = int(season_param) if season_param is not None else 1
    except ValueError:
        season = 1

    try:
        episode = int(episode_param) if episode_param is not None else 1
    except ValueError:
        episode = 1

    full_season = full_season_param in ("1", "true", "yes")

    # ✅ pass season/episode/full_season to scraper
    result = find_movie_link(
        tmdb_id=tmdb_id,
        imdb_id=imdb_id,
        title=title,
        is_tv=is_tv,
        season=season,
        episode=episode,
        full_season=full_season
    )

    if result:
        return jsonify(result)

    return jsonify({"success": False, "message": "Content not found on sources"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
