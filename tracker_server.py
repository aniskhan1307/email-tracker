from flask import Flask, request, send_file, redirect
import sqlite3, base64
from io import BytesIO
from datetime import datetime
import urllib.parse

app = Flask(__name__)
DB = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS opens (eid TEXT, time TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS clicks (eid TEXT, url TEXT, time TEXT)")
    conn.commit()
    conn.close()

@app.route("/track/open")
def open_track():
    eid = request.args.get("eid", "unknown")
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO opens VALUES (?,?)", (eid, datetime.utcnow()))
    conn.commit()
    conn.close()

    gif = base64.b64decode(
        "R0lGODlhAQABAPAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
    )
    return send_file(BytesIO(gif), mimetype="image/gif")

@app.route("/track/click")
def click_track():
    eid = request.args.get("eid", "unknown")
    url = urllib.parse.unquote_plus(request.args.get("url", "https://google.com"))
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO clicks VALUES (?,?,?)", (eid, url, datetime.utcnow()))
    conn.commit()
    conn.close()
    return redirect(url)

@app.route("/stats")
def stats():
    conn = sqlite3.connect(DB)
    opens = conn.execute("SELECT COUNT(*) FROM opens").fetchone()[0]
    clicks = conn.execute("SELECT COUNT(*) FROM clicks").fetchone()[0]
    conn.close()
    return {"opens": opens, "clicks": clicks}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
