import sqlite3
import random
try:
    from mcp.server.fastmcp import FastMCP
except (ImportError, ModuleNotFoundError):
    try:
        from fastmcp import FastMCP
    except Exception:
        class FastMCP:
            def __init__(self, *args, **kwargs):
                pass
            def tool(self, *args, **kwargs):
                def decorator(f):
                    return f
                return decorator

# Initialize MCP Server
mcp = FastMCP("CarePulse Clinic Service")

DB_FILE = "carepulse.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@mcp.tool()
def get_available_doctors(specialization: str = "") -> list:
    """Fetch list of doctors, their specialization, available days, hours, and fee.
    Can optionally filter by specialization (e.g. 'Cardiologist', 'Dermatologist')."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if specialization:
        cursor.execute(
            "SELECT id, name, specialization, available_days, timings, consultation_fee FROM doctors WHERE specialization LIKE ?",
            (f"%{specialization}%",)
        )
    else:
        cursor.execute("SELECT id, name, specialization, available_days, timings, consultation_fee FROM doctors")
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@mcp.tool()
def check_doctor_booked_slots(doctor_id: int, appointment_date: str) -> list:
    """Check all booked time slots for a specific doctor on a given date (YYYY-MM-DD)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT time_slot FROM appointments WHERE doctor_id = ? AND appointment_date = ? AND status != 'Cancelled'",
        (doctor_id, appointment_date)
    )
    rows = cursor.fetchall()
    conn.close()
    return [row["time_slot"] for row in rows]

@mcp.tool()
def book_appointment(patient_name: str, phone_number: str, doctor_id: int, appointment_date: str, time_slot: str) -> dict:
    """Book a new clinic appointment for a patient after confirming availability."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check for slot collision
    cursor.execute(
        "SELECT id FROM appointments WHERE doctor_id = ? AND appointment_date = ? AND time_slot = ? AND status != 'Cancelled'",
        (doctor_id, appointment_date, time_slot)
    )
    if cursor.fetchone():
        conn.close()
        return {"status": "error", "message": f"Time slot {time_slot} on {appointment_date} is already booked."}
    
    ref_id = f"CP-{random.randint(10000, 99999)}"
    cursor.execute(
        """INSERT INTO appointments (reference_id, patient_name, phone_number, doctor_id, appointment_date, time_slot, status)
           VALUES (?, ?, ?, ?, ?, ?, 'Confirmed')""",
        (ref_id, patient_name, phone_number, doctor_id, appointment_date, time_slot)
    )
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "reference_id": ref_id,
        "patient_name": patient_name,
        "appointment_date": appointment_date,
        "time_slot": time_slot,
        "message": f"Appointment confirmed successfully with Reference ID: {ref_id}"
    }

if __name__ == "__main__":
    mcp.run()