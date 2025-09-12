# api.py
from flask import Flask, request, jsonify
from scraper import find_movie_link
from flask_cors import CORS
import os

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

    result = find_movie_link(tmdb_id=tmdb_id, imdb_id=imdb_id, title=title, is_tv=is_tv)

    if result:
        return jsonify(result)

    return jsonify({"success": False, "message": "Content not found on sources"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
