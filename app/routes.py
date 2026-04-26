from flask import request, jsonify, render_template_string
from app import app
from app.db import (
    init_db,
    add_incident,
    get_all_incidents,
    delete_incident_db,
    add_audit_log,
    get_audit_logs,
    save_doctor_review,
    get_doctor_review
)

init_db()

current_user = {"name": "Admin"}


# ---------------- DASHBOARD ----------------
@app.route("/")
def home():

    incidents = get_all_incidents()
    logs = get_audit_logs()

    html = """
    <html>
    <head>
        <title>Clinical Incident Dashboard</title>

        <style>
            body { font-family: Arial; margin:0; background:#f4f7fb; }

            .header {
                background:#1f3b57;
                color:white;
                padding:15px;
                display:flex;
                justify-content:space-between;
                align-items:center;
            }

            .profile {
                width:38px;
                height:38px;
                border-radius:50%;
                background:white;
                color:#1f3b57;
                display:flex;
                align-items:center;
                justify-content:center;
                font-weight:bold;
                cursor:pointer;
                position:relative;
            }

            .dropdown {
                display:none;
                position:absolute;
                right:0;
                top:45px;
                background:white;
                border-radius:8px;
                box-shadow:0 2px 10px rgba(0,0,0,0.2);
            }

            .dropdown a {
                display:block;
                padding:10px;
                text-decoration:none;
                color:black;
            }

            .container { padding:20px; }

            table {
                width:100%;
                border-collapse:collapse;
                background:white;
                margin-top:10px;
            }

            th, td {
                padding:10px;
                border-bottom:1px solid #ddd;
            }

            th { background:#2c5282; color:white; }

            button {
                padding:8px 10px;
                cursor:pointer;
                margin:3px;
            }

            .modal {
                display:none;
                position:fixed;
                top:0; left:0;
                width:100%; height:100%;
                background:rgba(0,0,0,0.5);
            }

            .modal-content {
                background:white;
                padding:20px;
                width:400px;
                margin:10% auto;
                border-radius:10px;
            }

            textarea, input {
                width:100%;
                padding:8px;
                margin:6px 0;
            }
        </style>

        <script>
            function toggleProfile(){
                let d = document.getElementById("dropdown");
                d.style.display = d.style.display === "block" ? "none" : "block";
            }

            function openModal(){
                document.getElementById("modal").style.display = "block";
            }

            function closeModal(){
                document.getElementById("modal").style.display = "none";
            }

            function submitIncident(){
                fetch('/incident', {
                    method:'POST',
                    headers:{'Content-Type':'application/json'},
                    body: JSON.stringify({
                        resident_name: document.getElementById("name").value,
                        incident_type: document.getElementById("type").value,
                        severity: document.getElementById("severity").value,
                        description: document.getElementById("desc").value
                    })
                }).then(()=>location.reload());
            }

            function deleteIncident(id){
                fetch('/incident/' + id, {method:'DELETE'})
                .then(()=>location.reload());
            }

            function doctorReview(id){
                window.open("/doctor/" + id, "_blank");
            }

            function viewReport(id){
                window.open("/report/" + id, "_blank");
            }
        </script>

    </head>

    <body>

    <div class="header">
        <h2>🏥 Clinical Incident Dashboard</h2>

        <div class="profile" onclick="toggleProfile()">
            {{user[0].upper()}}

            <div class="dropdown" id="dropdown">
                <a href="#">Login</a>
                <a href="#">Sign Out</a>
            </div>
        </div>
    </div>

    <div class="container">

        <button onclick="openModal()">➕ Create Incident</button>

        <div class="modal" id="modal">
            <div class="modal-content">
                <h3>Create Incident</h3>

                <input id="name" placeholder="Resident Name">
                <input id="type" placeholder="Type">
                <input id="severity" placeholder="Severity">
                <textarea id="desc" placeholder="Description"></textarea>

                <button onclick="submitIncident()">Save</button>
                <button onclick="closeModal()">Cancel</button>
            </div>
        </div>

        <h3>Incidents</h3>

        <table>
            <tr>
                <th>Resident</th>
                <th>Type</th>
                <th>Status</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>

            {% for i in incidents %}
            <tr>
                <td>{{i.resident_name}}</td>
                <td>{{i.incident_type}}</td>
                <td>{{i.status}}</td>
                <td>{{i.description}}</td>
                <td>
                    <button onclick="doctorReview({{i.id}})">🩺 Doctor Review</button>
                    <button onclick="viewReport({{i.id}})">📄 Report</button>
                    <button onclick="deleteIncident({{i.id}})">🗑</button>
                </td>
            </tr>
            {% endfor %}
        </table>

        <h3>Audit Logs</h3>

        <table>
            <tr>
                <th>User</th>
                <th>Action</th>
                <th>Time</th>
            </tr>

            {% for l in logs %}
            <tr>
                <td>{{l.user}}</td>
                <td>{{l.action}}</td>
                <td>{{l.timestamp}}</td>
            </tr>
            {% endfor %}
        </table>

    </div>
    </body>
    </html>
    """

    return render_template_string(html, incidents=incidents, logs=logs, user=current_user["name"])


# ---------------- CREATE ----------------
@app.route("/incident", methods=["POST"])
def create():
    data = request.get_json()
    add_incident(data)
    add_audit_log(current_user["name"], "CREATED INCIDENT")
    return jsonify({"message": "created"})


# ---------------- DELETE ----------------
@app.route("/incident/<int:id>", methods=["DELETE"])
def delete(id):
    delete_incident_db(id)
    add_audit_log(current_user["name"], f"DELETED {id}")
    return jsonify({"message": "deleted"})


# ---------------- DOCTOR REVIEW ----------------
@app.route("/doctor/<int:id>")
def doctor_page(id):

    return f"""
    <html>
    <body style='font-family:Arial;padding:30px'>
    <h2>Doctor Review</h2>

    <input id="doctor" placeholder="Doctor Name"><br><br>
    <textarea id="notes" placeholder="Notes"></textarea><br><br>

    <button onclick="save()">Save</button>

    <script>
    function save(){{
        fetch('/doctor/{id}', {{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body: JSON.stringify({{
                doctor:document.getElementById('doctor').value,
                notes:document.getElementById('notes').value
            }})
        }}).then(()=>alert("Saved"));
    }}
    </script>
    </body>
    </html>
    """


@app.route("/doctor/<int:id>", methods=["POST"])
def save_doctor(id):
    data = request.get_json()
    save_doctor_review(id, data)
    add_audit_log(current_user["name"], f"DOCTOR REVIEW {id}")
    return jsonify({"ok": True})


# ---------------- REPORT ----------------
@app.route("/report/<int:id>")
def report(id):

    incidents = get_all_incidents()
    review = get_doctor_review(id)

    for i in incidents:
        if i["id"] == id:

            return f"""
            <html><body style='font-family:Arial;padding:30px'>
            <h2>Email Summary</h2>

            <textarea style='width:100%;height:300px'>
Dear Family,

We would like to inform you about an incident involving {i['resident_name']}.

Incident:
{i['description']}

Doctor Notes:
{review}

Regards,
Care Team
            </textarea>

            <br><br>
            <button onclick="alert('Email sent')">Send</button>

            </body></html>
            """

    return "Not found"