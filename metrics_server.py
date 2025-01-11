from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_last_10_metrics(db_name="face_data.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    connection.close()

    metrics = [
        {"id": row[0], "timestamp": row[1], "blink_count": row[2]} 
        for row in rows
    ]
    return metrics

@app.route('/metrics', methods=['GET'])
def metrics():
    try:
        data = get_last_10_metrics()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
