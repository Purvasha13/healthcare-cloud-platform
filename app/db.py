import sqlite3
from datetime import datetime

DB_NAME = "incidents.db"


# ---------------- INIT ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resident_name TEXT,
        incident_type TEXT,
        severity TEXT,
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
        incident_id INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------- INCIDENTS ----------------
def add_incident(data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO incidents (
            resident_name, incident_type, severity, description, status, time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("resident_name"),
        data.get("incident_type"),
        data.get("severity", "LOW"),
        data.get("description", ""),
        "OPEN",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_incidents():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM incidents ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "resident_name": r[1],
            "incident_type": r[2],
            "severity": r[3],
            "description": r[4],
            "status": r[5],
            "time": r[6]
        }
        for r in rows
    ]


def delete_incident_db(incident_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("DELETE FROM incidents WHERE id=?", (incident_id,))

    conn.commit()
    conn.close()


# ---------------- AUDIT ----------------
def add_audit_log(user, action, incident_id=None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO audit_logs (user, action, incident_id, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        user,
        action,
        incident_id,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_audit_logs():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM audit_logs ORDER BY id DESC")
    rows = cur.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "user": r[1],
            "action": r[2],
            "incident_id": r[3],
            "timestamp": r[4]
        }
        for r in rows
    ]