from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime

app = Flask(__name__)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="hotel",
    user="postgres",
    password="in950717",
    host="localhost"
)

@app.route("/", methods=["GET"])
def index():
    cur = conn.cursor()
    cur.execute("""
        SELECT name, room, check_in, check_out
        FROM BKI
        ORDER BY check_in DESC
    """)
    bookings = cur.fetchall()
    cur.close()
    return render_template("index.html", bookings=bookings)

@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        room = request.form["room"]
        check_in = request.form["check_in"]
        check_out = request.form["check_out"]

        # 🔴 Date validation
        if check_out <= check_in:
            return render_template(
                "booking.html",
                error="Check-out date must be later than check-in date."
            )

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO BKI (name, room, check_in, check_out)
            VALUES (%s, %s, %s, %s)
        """, (name, room, check_in, check_out))
        conn.commit()
        cur.close()

        return redirect(url_for("index"))

    return render_template("booking.html")

if __name__ == '__main__':
    app.run(debug=True)
