from flask import Flask, render_template, jsonify, request
import pyodbc

app = Flask(__name__)

DB_CONFIG = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PHCSystemDB;"
    "Trusted_Connection=yes;"
)

def get_db_connection():
    return pyodbc.connect(DB_CONFIG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/locations", methods=["GET"])
def get_locations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT LocationID, LocationName FROM Locations")
        locations = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        conn.close()
        return jsonify({"success": True, "locations": locations})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/doctors/<int:location_id>", methods=["GET"])
def get_doctors_by_location(location_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DoctorID, DoctorName, Department_EN, Department_TE, RoomNo, IsAvailable 
            FROM Doctors WHERE LocationID = ?
        """, location_id)
        doctors = []
        for row in cursor.fetchall():
            doctors.append({
                "id": row[0],
                "name": row[1],
                "dept_en": row[2],
                "dept_te": row[3],
                "room": row[4],
                "available": bool(row[5])
            })
        conn.close()
        return jsonify({"success": True, "doctors": doctors})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/book", methods=["POST"])
def book_appointment():
    data = request.json
    uid = data.get("uid")
    name = data.get("name")
    doctor_id = data.get("doctor_id")
    location_id = data.get("location_id")
    slot = data.get("slot")
    appt_date = data.get("date")  # New Date Parameter

    if not all([uid, name, doctor_id, location_id, slot, appt_date]):
        return jsonify({"success": False, "message": "Missing required details"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Calculate daily token sequence for that specific doctor and date
        cursor.execute("SELECT COUNT(*) FROM Appointments WHERE DoctorID = ? AND AppointmentDate = ?", doctor_id, appt_date)
        token_number = cursor.fetchone()[0] + 1

        cursor.execute("""
            INSERT INTO Appointments (PatientUID, PatientName, DoctorID, LocationID, Slot, TokenNumber, BookingStatus, AppointmentDate)
            VALUES (?, ?, ?, ?, ?, ?, 'Confirmed', ?)
        """, uid, name, doctor_id, location_id, slot, token_number, appt_date)
        conn.commit()
        conn.close()

        return jsonify({"success": True, "token_number": token_number, "message": "Appointment booked successfully."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/patient-status/<uid>", methods=["GET"])
def get_patient_status(uid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.AppointmentID, a.PatientName, d.DoctorName, d.Department_EN, l.LocationName, d.RoomNo, a.Slot, a.TokenNumber, a.BookingStatus, a.AppointmentDate
            FROM Appointments a
            JOIN Doctors d ON a.DoctorID = d.DoctorID
            JOIN Locations l ON a.LocationID = l.LocationID
            WHERE a.PatientUID = ?
            ORDER BY a.AppointmentID DESC
        """, uid)
        
        appointments = []
        for row in cursor.fetchall():
            appointments.append({
                "id": row[0],
                "patient_name": row[1],
                "doctor_name": row[2],
                "department": row[3],
                "location": row[4],
                "room": row[5],
                "slot": row[6],
                "token": row[7],
                "status": row[8],
                "date": str(row[9])[:10]
            })
        conn.close()
        return jsonify({"success": True, "appointments": appointments})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/patient-reports/<uid>", methods=["GET"])
def get_patient_reports(uid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ReportID, DoctorName, ReportTitle, ReportDate, DiagnosisSummary, Status
            FROM PatientReports
            WHERE PatientUID = ?
            ORDER BY ReportDate DESC
        """, uid)
        reports = []
        for row in cursor.fetchall():
            reports.append({
                "id": row[0],
                "doctor": row[1],
                "title": row[2],
                "date": str(row[3]),
                "summary": row[4],
                "status": row[5]
            })
        conn.close()
        return jsonify({"success": True, "reports": reports})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/doctor/availability", methods=["POST"])
def toggle_availability():
    data = request.json
    doctor_id = data.get("doctor_id")
    available = 1 if data.get("available") else 0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Doctors SET IsAvailable = ? WHERE DoctorID = ?", available, doctor_id)
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Doctor status updated in DB."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)