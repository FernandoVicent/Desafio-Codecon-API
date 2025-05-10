from flask import Flask, request
from storage import save_users, get_users
from utils import timed_route
from collections import defaultdict, Counter
import json
import requests
import time

app = Flask(__name__)

@app.route("/users", methods=["POST"])
@timed_route
def load_users():
    if 'file' not in request.files:
        return {"error": "No file part in request"}, 400

    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400

    try:
        users_data = json.load(file)
        save_users(users_data)
        return {"status": "ok", "received": len(users_data)}
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/superusers", methods=["GET"])
@timed_route
def get_superusers():
    superusers = [u for u in get_users() if u.get("active") and u.get("score", 0) >= 900]
    return {"superusers": superusers}

@app.route("/top-countries", methods=["GET"])
@timed_route
def top_countries():
    superusers = [u for u in get_users() if u.get("active") and u.get("score", 0) >= 900]
    counts = Counter(u["country"] for u in superusers)
    top = counts.most_common(5)
    return {"top_countries": [{"country": c, "count": n} for c, n in top]}

@app.route("/team-insights", methods=["GET"])
@timed_route
def team_insights():
    insights = defaultdict(lambda: {"members": 0, "leaders": 0, "completed_projects": 0, "active_percent": 0})
    users = get_users()

    for u in users:
        t = u["team"]["name"]
        insights[t]["members"] += 1
        if u["team"].get("leader"):
            insights[t]["leaders"] += 1
        insights[t]["completed_projects"] += sum(1 for p in u["team"]["projects"] if p["completed"])

    for team in insights:
        members = [u for u in users if u["team"]["name"] == team]
        actives = sum(1 for u in members if u.get("active"))
        total = len(members)
        insights[team]["active_percent"] = round(100 * actives / total, 2)

    return {"teams": insights}

@app.route("/active-users-per-day", methods=["GET"])
@timed_route
def logins_by_day():
    min_logins = int(request.args.get("min", 0))
    count = defaultdict(int)

    for u in get_users():
        for log in u.get("logs", []):
            if log["action"] == "login":
                count[log["date"]] += 1

    result = {d: n for d, n in count.items() if n >= min_logins}
    return {"logins": result}

@app.route("/evaluation", methods=["GET"])
@timed_route
def evaluate():


    base = "http://localhost:5000"
    endpoints = [
        "/superusers",
        "/top-countries",
        "/team-insights",
        "/active-users-per-day"
    ]

    results = []

    for ep in endpoints:
        full_url = base + ep
        try:
            start = time.time()
            res = requests.get(full_url)
            duration = round((time.time() - start) * 1000, 2)

            # Tenta validar o JSON
            try:
                _ = res.json()
                valid_json = True
            except Exception:
                valid_json = False

            results.append({
                "endpoint": ep,
                "status_code": res.status_code,
                "valid_json": valid_json,
                "response_time_ms": duration
            })
        except Exception as e:
            results.append({
                "endpoint": ep,
                "error": str(e)
            })

    return {"evaluation": results}

if __name__ == '__main__':
    app.run(debug=True)