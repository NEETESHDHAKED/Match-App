from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
FILE = "cricket.json"

def load():
    if os.path.exists(FILE):
        try:
            with open(FILE) as f:
                data = json.load(f)
                for i,p in enumerate(data): p["id"]=i
                return data
        except: return []
    return []

def save(d):
    for p in d:
        if "id" in p: del p["id"]
    with open(FILE,"w") as f: json.dump(d,f)

@app.route("/")
def home():
    matches = load()
    q = request.args.get("q","")
    res = []
    if q:
        res = [p for p in matches if q.lower() in p['team1'].lower() or q.lower() in p['team2'].lower() or q.lower() in p['village'].lower()]
    total = len(matches)
    players = {}
    for m in matches:
        if m.get('batsman'):
            try: players[m['batsman']] = players.get(m['batsman'],0) + int(m.get('batsman_run') or 0)
            except: pass
    top = sorted(players.items(), key=lambda x: x[1], reverse=True)[:5]
    return render_template("cricket.html", matches=matches, res=res, q=q, total=total, top=top)

@app.route("/add", methods=["POST"])
def add():
    d = load()
    d.append({
        "team1": request.form["team1"],
        "team2": request.form["team2"],
        "score1": request.form["score1"],
        "score2": request.form["score2"],
        "over": request.form["over"],
        "village": request.form["village"],
        "batsman": request.form["batsman"],
        "batsman_run": request.form["batsman_run"],
        "bowler": request.form["bowler"],
        "winner": request.form["winner"],
        "status": request.form["status"],
        "price": request.form["price"]
    })
    save(d)
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    d = load()
    if id < len(d):
        d[id]["score1"] = request.form["score1"]
        d[id]["score2"] = request.form["score2"]
        d[id]["batsman"] = request.form["batsman"]
        d[id]["batsman_run"] = request.form["batsman_run"]
        d[id]["over"] = request.form["over"]
        d[id]["winner"] = request.form["winner"]
        d[id]["status"] = request.form["status"]
        save(d)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    d = load()
    if id < len(d): d.pop(id); save(d)
    return redirect("/")

@app.route("/match/<int:id>")
def match(id):
    all_m = load()
    if id >= len(all_m): return redirect("/")
    m = all_m[id]
    return render_template("match.html", m=m, id=id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
