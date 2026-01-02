from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="hotel",
    user="postgres",
    password="in950717",
    host="localhost",
    port = "5432"
)

@app.route("/admin")
def admin_home():
    return render_template("admin.html")

@app.route("/admin/search", methods=["POST"])
def admin_search():
    booking_id = request.form.get("booking_id")
    guest_name = request.form.get("guest_name")
    date_from = request.form.get("date_from")
    date_to = request.form.get("date_to")

    cur = conn.cursor()

    sql = "SELECT booking_id, room_number, guest_name, phone, check_in, check_out FROM booking WHERE 1=1"
    params = []

    if booking_id:
        sql += " AND booking_id = %s"
        params.append(booking_id)

    if guest_name:
        sql += " AND guest_name ILIKE %s"
        params.append("%" + guest_name + "%")

    if date_from:
        sql += " AND check_in >= %s"
        params.append(date_from)

    if date_to:
        sql += " AND check_out <= %s"
        params.append(date_to)

    cur.execute(sql, params)
    results = cur.fetchall()
    cur.close()

    # 把查詢結果傳給 admin.html
    return render_template("admin.html", results=results)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search_booking", methods=["POST"])
def search_booking():
    booking_id = request.form.get("booking_id")

    # 檢查輸入是不是數字
    if not booking_id.isdigit():
        return render_template("index.html", not_found=True)

    booking_id = int(booking_id)  # 轉成整數

    cur = conn.cursor()
    cur.execute("""
        SELECT room_number, check_in, check_out 
        FROM booking WHERE booking_id = %s
    """, (booking_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        # row 會是 tuple (room_number, check_in, check_out)
        return render_template("index.html", result=row)
    else:
        return render_template("index.html", not_found=True)

    
if __name__ == '__main__':
    app.run(debug=True)