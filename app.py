from flask import Flask, render_template, request, redirect, url_for
import random
import time
import os

app = Flask(__name__)

LEADERBOARD_FILE = "leaderboard.txt"
game_data = {}

def save_score(name, score):
    with open(LEADERBOARD_FILE, "a") as f:
        f.write(f"{name},{score}\n")

def get_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    scores = []
    with open(LEADERBOARD_FILE, "r") as f:
        for line in f:
            name, score = line.strip().split(",")
            scores.append((name, int(score)))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:5]

@app.route("/", methods=["GET", "POST"])
def index():
    global game_data

    if request.method == "POST":
        if "start" in request.form:
            difficulty = request.form["difficulty"]

            if difficulty == "easy":
                max_num, attempts, multiplier = 10, 5, 1
            elif difficulty == "medium":
                max_num, attempts, multiplier = 50, 7, 2
            else:
                max_num, attempts, multiplier = 100, 10, 3

            game_data = {
                "number": random.randint(1, max_num),
                "attempts": attempts,
                "multiplier": multiplier,
                "start_time": time.time(),
                "max_num": max_num
            }

            return render_template("index.html", game=game_data)

        elif "guess" in request.form:
            guess = int(request.form["guess"])
            game_data["attempts"] -= 1

            if guess < game_data["number"]:
                message = "Too Low!"
            elif guess > game_data["number"]:
                message = "Too High!"
            else:
                time_taken = time.time() - game_data["start_time"]
                time_bonus = max(0, 60 - int(time_taken))
                score = (game_data["attempts"] * 10 + time_bonus) * game_data["multiplier"]

                name = request.form["name"]
                save_score(name, score)

                return redirect(url_for("leaderboard"))

            if game_data["attempts"] == 0:
                message = f"Game Over! Number was {game_data['number']}"

            return render_template("index.html", game=game_data, message=message)

    return render_template("index.html")

@app.route("/leaderboard")
def leaderboard():
    scores = get_leaderboard()
    return render_template("leaderboard.html", scores=scores)

if __name__ == "__main__":
    app.run(debug=True)
