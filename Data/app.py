from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Database connection parameters
dbname = "hotel"
user = "postgres"
password = "in950717"
host = "localhost"

@app.route('/')
def index():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()
    cur.execute('SELECT check_in_date, check_out_date, booker_name FROM "BookOrder"')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
