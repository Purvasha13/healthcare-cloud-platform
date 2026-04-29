import sqlite3
from datetime import datetime

DB_NAME = "incidents.db"


# ---------------- INIT DB ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_name TEXT,
        room_no TEXT,
        incident_type TEXT,
        description TEXT,
        status TEXT,
        time TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS doctor_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id INTEGER,
        doctor TEXT,
        notes TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- ADD INCIDENT ----------------
def add_incident(data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO incidents 
        (resident_name, room_no, incident_type, description, status, time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("resident_name"),
        data.get("room_no"),
        data.get("incident_type"),
        data.get("description"),
        "OPEN",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ---------------- GET INCIDENTS ----------------
def get_all_incidents():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM incidents ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    incidents = []

    for r in rows:
        incidents.append({
            "id": r[0],
            "resident_name": r[1],
            "room_no": r[2],
            "incident_type": r[3],
            "description": r[4],
            "status": r[5],
            "time": r[6]
        })

    return incidents


# ---------------- DELETE ----------------
def delete_incident_db(incident_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM incidents WHERE id=?", (incident_id,))

    conn.commit()
    conn.close()


# ---------------- AUDIT ----------------
def add_audit_log(user, action):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audit_logs (user, action, timestamp)
        VALUES (?, ?, ?)
    """, (
        user,
        action,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_audit_logs():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT user, action, timestamp FROM audit_logs ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    return [{"user": r[0], "action": r[1], "timestamp": r[2]} for r in rows]


# ---------------- DOCTOR REVIEW ----------------
def save_doctor_review(incident_id, data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO doctor_reviews (incident_id, doctor, notes, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        incident_id,
        data.get("doctor"),
        data.get("notes"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    cur.execute("""
        UPDATE incidents
        SET status = 'DOCTOR_REVIEWED'
        WHERE id = ?
    """, (incident_id,))

    conn.commit()
    conn.close()


def get_doctor_review(incident_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT doctor, notes, timestamp
        FROM doctor_reviews
        WHERE incident_id = ?
        ORDER BY id DESC LIMIT 1
    """, (incident_id,))

    row = cur.fetchone()
    conn.close()

    if row:
        return f"Doctor: {row[0]}\nNotes: {row[1]}\nTime: {row[2]}"

    return ""