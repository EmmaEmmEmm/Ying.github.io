const API_BASE = "http://127.0.0.1:5000/api";

// Users
async function createUser(data) {
    return fetch(`${API_BASE}/users`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}

async function getUsers() {
    const res = await fetch(`${API_BASE}/users`);
    return res.json();
}

// Services
async function getServices() {
    const res = await fetch(`${API_BASE}/services`);
    return res.json();
}

// Bookings
async function createBooking(data) {
    return fetch(`${API_BASE}/bookings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
}
