from flask import Flask, request, jsonify, render_template
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection parameters
dbname = "hotel"
user = "postgres"
password = "in950717"
host = "localhost"

def get_conn():
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

# ---------------------------
# Home Page: Show BookOrders
# ---------------------------
@app.route('/')
def index():
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute('SELECT check_in_date, check_out_date, booker_name FROM "BookOrder"')
    data = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('index.html', data=data)


# ---------------------------
# API: Users
# ---------------------------
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (name, email, contact) VALUES (%s, %s, %s) RETURNING user_id',
        (data['name'], data['email'], data.get('contact'))
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'User created', 'user_id': user_id}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT user_id, name, email, contact FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    result = [{'user_id': u[0], 'name': u[1], 'email': u[2], 'contact': u[3]} for u in users]
    return jsonify(result)


# ---------------------------
# API: Services
# ---------------------------
@app.route('/api/services', methods=['POST'])
def create_service():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO services (service_name, description, price) VALUES (%s, %s, %s) RETURNING service_id',
        (data['service_name'], data.get('description'), data['price'])
    )
    service_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Service created', 'service_id': service_id}), 201

@app.route('/api/services', methods=['GET'])
def get_services():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT service_id, service_name, description, price FROM services')
    services = cur.fetchall()
    cur.close()
    conn.close()
    result = [{'service_id': s[0], 'service_name': s[1], 'description': s[2], 'price': float(s[3])} for s in services]
    return jsonify(result)


# ---------------------------
# API: Bookings
# ---------------------------
@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    conn = get_conn()
    cur = conn.cursor()
    booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
    booking_time = datetime.strptime(data['booking_time'], '%H:%M').time()
    
    cur.execute(
        'INSERT INTO bookings (user_id, service_id, booking_date, booking_time, status) VALUES (%s, %s, %s, %s, %s) RETURNING booking_id',
        (data['user_id'], data['service_id'], booking_date, booking_time, 'active')
    )
    booking_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Booking created', 'booking_id': booking_id}), 201

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT booking_id, user_id, service_id, booking_date, booking_time, status FROM bookings')
    bookings = cur.fetchall()
    cur.close()
    conn.close()
    
    result = []
    for b in bookings:
        result.append({
            'booking_id': b[0],
            'user_id': b[1],
            'service_id': b[2],
            'booking_date': b[3].strftime('%Y-%m-%d'),
            'booking_time': b[4].strftime('%H:%M'),
            'status': b[5]
        })
    return jsonify(result)

@app.route('/admin')
def admin_dashboard():
    conn = get_conn()
    cur = conn.cursor()

    # Users
    cur.execute('SELECT user_id, name, email, contact FROM users')
    users = cur.fetchall()

    # Services
    cur.execute('SELECT service_id, service_name, description, price FROM services')
    services = cur.fetchall()

    # Bookings
    cur.execute('SELECT booking_id, user_id, service_id, booking_date, booking_time, status FROM bookings')
    bookings = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('admin.html', users=users, services=services, bookings=bookings)
if __name__ == '__main__':
    app.run(debug=True)
