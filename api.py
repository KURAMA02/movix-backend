# api.py
from flask import Flask, request, jsonify
from scraper import find_movie_link
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "Backend is running!"})


if __name__ == "__main__":
    app.run()

@app.route("/find_movie", methods=["GET"])
def find_movie():
    tmdb_id = request.args.get("tmdb_id")
    imdb_id = request.args.get("imdb_id")
    title = request.args.get("title")

    result = find_movie_link(tmdb_id=tmdb_id, imdb_id=imdb_id, title=title)

    if result:
        return jsonify(result)

    return jsonify({"success": False, "message": "Movie not found on sources"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
