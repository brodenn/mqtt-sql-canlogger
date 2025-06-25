import os
import psycopg2
import csv
from io import StringIO
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "candb"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASS", "password"),
        host=os.getenv("DB_HOST", "db")
    )

def fetch_query(sql, params=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            cols = [desc[0] for desc in cursor.description]
            return [dict(zip(cols, row)) for row in cursor.fetchall()]

@app.route("/")
def root():
    return jsonify({
        "views": [
            "/avg",
            "/latest",
            "/minute",
            "/extremes",
            "/count_per_topic",
            "/latest_by_name?topic=canbus/temp",
            "/history?limit=100",
            "/export.csv?limit=1000"
        ],
        "status": "OK"
    })

@app.route("/avg")
def avg():
    return jsonify(fetch_query("SELECT * FROM avg_recent_values"))

@app.route("/latest")
def latest():
    return jsonify(fetch_query("SELECT * FROM latest_per_topic"))

@app.route("/minute")
def minute():
    return jsonify(fetch_query("SELECT * FROM messages_per_minute"))

@app.route("/extremes")
def extremes():
    return jsonify(fetch_query("SELECT * FROM extremes_recent"))

@app.route("/count_per_topic")
def count_per_topic():
    return jsonify(fetch_query("""
        SELECT t.name, COUNT(m.id) as message_count
        FROM topics t
        JOIN messages m ON t.id = m.topic_id
        GROUP BY t.name
        ORDER BY message_count DESC
    """))

@app.route("/latest_by_name")
def latest_by_name():
    topic = request.args.get("topic")
    if not topic:
        return jsonify({"error": "Missing topic parameter"}), 400
    return jsonify(fetch_query("""
        SELECT t.name, m.timestamp, m.payload
        FROM messages m
        JOIN topics t ON m.topic_id = t.id
        WHERE t.name = %s
        ORDER BY m.timestamp DESC
        LIMIT 1
    """, (topic,)))

@app.route("/history")
def history():
    limit = request.args.get("limit", default=100, type=int)
    return jsonify(fetch_query("""
        SELECT t.name, m.timestamp, m.payload
        FROM messages m
        JOIN topics t ON m.topic_id = t.id
        ORDER BY m.timestamp DESC
        LIMIT %s
    """, (limit,)))

@app.route("/export.csv")
def export_csv():
    limit = request.args.get("limit", default=1000, type=int)
    rows = fetch_query("""
        SELECT t.name, m.timestamp, m.payload
        FROM messages m
        JOIN topics t ON m.topic_id = t.id
        ORDER BY m.timestamp DESC
        LIMIT %s
    """, (limit,))

    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=["name", "timestamp", "payload"])
    writer.writeheader()
    writer.writerows(rows)
    output = si.getvalue()

    return Response(output, mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=canlog.csv"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
