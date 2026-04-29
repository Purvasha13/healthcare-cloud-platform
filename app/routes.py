from flask import request, jsonify, render_template_string
from app import app
from app.db import *

init_db()

current_user = {"name": "Admin"}


# ================= DASHBOARD =================
@app.route("/")
def home():

    incidents = get_all_incidents()
    logs = get_audit_logs()

    html = """
    <html>
    <head>
    <title>Clinical Incident System</title>

    <style>
    body {
        margin:0;
        font-family:'Segoe UI', Arial;
        background:#f4f6f9;
    }

    /* TOP BAR */
    .topbar {
        height:60px;
        background:white;
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding:0 20px;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
        position:fixed;
        width:100%;
        top:0;
        left:0;
        z-index:1000;
    }

    .title {
        font-size:18px;
        font-weight:600;
        color:#1f3b57;
    }

    /* PROFILE */
    .profile {
        position:relative;
        cursor:pointer;
        margin-right:40px;
    }

    .avatar {
        width:38px;
        height:38px;
        border-radius:50%;
        background:#2c5282;
        color:white;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:bold;
    }

    .dropdown {
        display:none;
        position:absolute;
        right:0;
        top:45px;
        background:white;
        min-width:140px;
        border-radius:10px;
        box-shadow:0 8px 20px rgba(0,0,0,0.12);
        overflow:hidden;
    }

    .dropdown div {
        padding:12px 15px;
        cursor:pointer;
        font-size:14px;
    }

    .dropdown div:hover {
        background:#f3f4f6;
    }

    /* SIDEBAR */
    .sidebar {
        width:220px;
        height:100vh;
        background:#1f3b57;
        color:white;
        position:fixed;
        top:60px;
        left:0;
    }

    .sidebar a {
        display:block;
        padding:14px 20px;
        color:white;
        text-decoration:none;
        font-size:15px;
    }

    .sidebar a:hover {
        background:#2c5282;
    }

    /* MAIN */
    .main {
        margin-left:220px;
        margin-top:60px;
        padding:25px;
    }

    /* CARD */
    .card {
        background:white;
        padding:22px;
        border-radius:14px;
        box-shadow:0 3px 10px rgba(0,0,0,0.06);
    }

    /* TABLE */
    table {
        width:100%;
        border-collapse:collapse;
        margin-top:15px;
    }

    th {
        text-align:left;
        padding:14px;
        font-size:13px;
        color:#666;
        background:#f8fafc;
        border-bottom:1px solid #e5e7eb;
    }

    td {
        padding:14px;
        border-bottom:1px solid #edf2f7;
        font-size:14px;
    }

    tr:hover {
        background:#f9fbfd;
    }

    /* STATUS */
    .badge {
        padding:6px 12px;
        border-radius:20px;
        font-size:12px;
        font-weight:600;
    }

    .open {
        background:#fee2e2;
        color:#b91c1c;
    }

    .reviewed {
        background:#ffedd5;
        color:#c2410c;
    }

    .closed {
        background:#dcfce7;
        color:#166534;
    }

    /* BUTTONS */
    button {
        border:none;
        padding:7px 12px;
        border-radius:7px;
        cursor:pointer;
        font-size:13px;
        margin:2px;
    }

    .btn-primary {
        background:#2c5282;
        color:white;
    }

    .btn-primary:hover {
        background:#1f3b57;
    }

    .btn-danger {
        background:#dc2626;
        color:white;
    }

    .btn-danger:hover {
        background:#b91c1c;
    }

    /* MODAL */
    .modal {
        display:none;
        position:fixed;
        top:0;
        left:0;
        width:100%;
        height:100%;
        background:rgba(0,0,0,0.45);
        z-index:2000;
    }

    .modal-content {
        background:white;
        width:440px;
        margin:7% auto;
        padding:24px;
        border-radius:14px;
        box-shadow:0 10px 25px rgba(0,0,0,0.15);
    }

    input, select, textarea {
        width:100%;
        padding:10px;
        margin:8px 0;
        border:1px solid #d1d5db;
        border-radius:8px;
        font-size:14px;
        box-sizing:border-box;
    }

    textarea {
        min-height:90px;
        resize:vertical;
    }

    h3 {
        margin:0 0 15px 0;
        color:#1f2937;
    }
    </style>

    <script>
    function toggleProfile(){
        let d = document.getElementById("dropdown");
        d.style.display = (d.style.display === "block") ? "none" : "block";
    }

    function openModal(){
        document.getElementById("modal").style.display = "block";
    }

    function closeModal(){
        document.getElementById("modal").style.display = "none";
    }

    function handleTypeChange(){
        let type = document.getElementById("type").value;
        let sirs = document.getElementById("sirs_type");

        if(type === "SIRS"){
            sirs.style.display = "block";
        } else {
            sirs.style.display = "none";
        }
    }

    function submitIncident(){

        let type = document.getElementById("type").value;
        let finalType = type;

        if(type === "SIRS"){
            finalType = "SIRS - " + document.getElementById("sirs_type").value;
        }

        fetch('/incident', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({
                resident_name: document.getElementById("name").value,
                room_no: document.getElementById("room").value,
                incident_type: finalType,
                description: document.getElementById("desc").value
            })
        }).then(()=>location.reload());
    }

    function deleteIncident(id){
        fetch('/incident/' + id, {
            method:'DELETE'
        }).then(()=>location.reload());
    }

    function doctorReview(id){
        window.open('/doctor/' + id, '_blank', 'width=700,height=650');
    }

    function viewReport(id){
        window.open('/report/' + id, '_blank');
    }

    window.onclick = function(event){
        let modal = document.getElementById("modal");
        if(event.target == modal){
            closeModal();
        }
    }
    </script>

    </head>

    <body>

    <!-- TOPBAR -->
    <div class="topbar">
        <div class="title">🏥 Clinical Incident System</div>

        <div class="profile" onclick="toggleProfile()">
            <div class="avatar">A</div>

            <div class="dropdown" id="dropdown">
                <div>👤 Login</div>
                <div>🚪 Sign Out</div>
            </div>
        </div>
    </div>

    <!-- SIDEBAR -->
    <div class="sidebar">
        <a href="/">📊 Dashboard</a>
        <a href="/">📜 Audit Logs</a>
    </div>

    <!-- MAIN -->
    <div class="main">

        <div class="card">

            <button class="btn-primary" onclick="openModal()">➕ Create Incident</button>

            <!-- MODAL -->
            <div id="modal" class="modal">
                <div class="modal-content">

                    <h3>Create New Incident</h3>

                    <input id="name" placeholder="Resident Name">
                    <input id="room" placeholder="Room Number">

                    <select id="type" onchange="handleTypeChange()">
                        <option>Fall</option>
                        <option>Medication Error</option>
                        <option>Behavioral Issue</option>
                        <option>SIRS</option>
                        <option>Other</option>
                    </select>

                    <select id="sirs_type" style="display:none;">
                        <option>Abuse</option>
                        <option>Neglect</option>
                        <option>Unexplained Absence</option>
                        <option>Psychological Harm</option>
                    </select>

                    <textarea id="desc" placeholder="Incident Description"></textarea>

                    <button class="btn-primary" onclick="submitIncident()">Save</button>
                    <button onclick="closeModal()">Cancel</button>

                </div>
            </div>

            <h3 style="margin-top:20px;">Incident Register</h3>

            <table>
                <tr>
                    <th>Resident</th>
                    <th>Room</th>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>

                {% for i in incidents %}
                <tr>
                    <td>{{i.resident_name}}</td>
                    <td>{{i.room_no}}</td>
                    <td>{{i.incident_type}}</td>
                    <td>{{i.description}}</td>
                    <td>
                        <span class="badge {% if i.status == 'OPEN' %}open{% elif i.status == 'DOCTOR_REVIEWED' %}reviewed{% else %}closed{% endif %}">
                            {{i.status}}
                        </span>
                    </td>
                    <td>
                        <button class="btn-primary" onclick="doctorReview({{i.id}})">Doctor</button>
                        <button class="btn-primary" onclick="viewReport({{i.id}})">Report</button>
                        <button class="btn-danger" onclick="deleteIncident({{i.id}})">Delete</button>
                    </td>
                </tr>
                {% endfor %}
            </table>

        </div>

    </div>
    <!-- AUDIT LOGS -->
        <div id="auditlogs" style="display:none;">

            <div class="card">

                <h3>Audit Logs</h3>

                <table>
                    <tr>
                        <th>User</th>
                        <th>Action</th>
                        <th>Timestamp</th>
                    </tr>

                    {% for log in logs %}
                    <tr>
                        <td>{{log.user}}</td>
                        <td>{{log.action}}</td>
                        <td>{{log.timestamp}}</td>
                    </tr>
                    {% endfor %}

                </table>

            </div>

        </div>

    </div>

    </body>
    </html>
    """

    return render_template_string(html, incidents=incidents, logs=logs)


# ================= CREATE =================
@app.route("/incident", methods=["POST"])
def create():
    data = request.get_json()
    add_incident(data)
    add_audit_log(current_user["name"], "CREATED INCIDENT")
    return jsonify({"ok": True})


# ================= DELETE =================
@app.route("/incident/<int:id>", methods=["DELETE"])
def delete(id):
    delete_incident_db(id)
    add_audit_log(current_user["name"], f"DELETED {id}")
    return jsonify({"ok": True})

# ================= DOCTOR REVIEW =================
@app.route("/doctor/<int:id>", methods=["GET", "POST"])
def doctor(id):

    if request.method == "POST":
        data = request.get_json()
        save_doctor_review(id, data)
        add_audit_log(current_user["name"], f"DOCTOR REVIEW {id}")
        return jsonify({"ok": True})

    review = get_doctor_review(id)

    return f"""
    <html>
    <head>
    <style>
    body {{
        font-family:Segoe UI;
        background:#f4f6f9;
        padding:30px;
    }}

    .card {{
        background:white;
        padding:25px;
        border-radius:12px;
        max-width:650px;
        margin:auto;
        box-shadow:0 4px 14px rgba(0,0,0,.08);
    }}

    input, textarea {{
        width:100%;
        padding:10px;
        margin:8px 0;
        border:1px solid #ddd;
        border-radius:8px;
        box-sizing:border-box;
    }}

    textarea {{
        height:180px;
    }}

    button {{
        background:#2c5282;
        color:white;
        border:none;
        padding:10px 16px;
        border-radius:8px;
        cursor:pointer;
    }}
    </style>
    </head>

    <body>
    <div class="card">

        <h2>🩺 Doctor Review</h2>

        <input id="doctor" placeholder="Doctor Name">

        <textarea id="notes">{review}</textarea>

        <button onclick="save()">Save Review</button>

    </div>

    <script>
    function save(){{
        fetch('/doctor/{id}', {{
            method:'POST',
            headers:{{'Content-Type':'application/json'}},
            body: JSON.stringify({{
                doctor: document.getElementById('doctor').value,
                notes: document.getElementById('notes').value
            }})
        }}).then(()=>alert("Saved Successfully"));
    }}
    </script>

    </body>
    </html>
    """

# ================= REPORT =================
@app.route("/report/<int:id>")
def report(id):

    incidents = get_all_incidents()
    review = get_doctor_review(id)

    for i in incidents:
        if i["id"] == id:

            email = f"""
Dear Family Member,

We are writing to update you regarding {i['resident_name']}.

An incident occurred today involving the following:

Room Number: {i['room_no']}
Incident Type: {i['incident_type']}

Description:
{i['description']}

Clinical Review:
{review}

Current Status: {i['status']}

Our team is monitoring the resident closely and appropriate care has been provided.

Please contact us if you have any questions.

Kind regards,
Clinical Care Team
"""

            return f"""
            <html>
            <body style="font-family:Segoe UI;background:#f4f6f9;padding:30px;">

            <div style="background:white;padding:25px;border-radius:12px;max-width:800px;margin:auto;box-shadow:0 4px 14px rgba(0,0,0,.08);">

                <h2>📄 Family Email Report</h2>

                <select style="padding:10px;margin-bottom:10px;">
                    <option>Send to Family</option>
                    <option>Send to Manager</option>
                </select>

                <textarea style="width:100%;height:350px;padding:10px;">{email}</textarea>

                <br><br>

                <button onclick="alert('Email Sent Successfully')"
                style="background:#2c5282;color:white;border:none;padding:10px 16px;border-radius:8px;">
                Send Email
                </button>

            </div>

            </body>
            </html>
            """

    return "Not found"