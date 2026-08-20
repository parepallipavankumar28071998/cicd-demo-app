from flask import Flask, jsonify, request, redirect, render_template
import sqlite3, string, random

app = Flask(__name__)
DB = "urls.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS urls (code TEXT PRIMARY KEY, original TEXT)")
    conn.commit()
    conn.close()

def make_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    original = data.get("url")
    if not original:
        return jsonify(error="url is required"), 400
    code = make_code()
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO urls (code, original) VALUES (?, ?)", (code, original))
    conn.commit()
    conn.close()
    return jsonify(short_code=code)

@app.route("/<code>")
def go(code):
    conn = sqlite3.connect(DB)
    row = conn.execute("SELECT original FROM urls WHERE code=?", (code,)).fetchone()
    conn.close()
    if row:
        return redirect(row[0])
    return jsonify(error="not found"), 404

init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
