import sqlite3
from typing import Optional
from langchain_core.tools import tool

DB_NAME = "clinic.db"

@tool
def get_available_doctors(speciality: Optional[str] = "") -> str:
    """Get list of doctors, their specialization, available days, timing, and fee.
    Pass speciality as empty string "" if asking for all doctors, or pass a filter like 'Dentist', 'Skin', 'General Physician'.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if speciality and speciality.strip():
        query = "SELECT id, name, speciality, days, timings, fee FROM doctors WHERE speciality LIKE ?"
        cursor.execute(query, (f"%{speciality.strip()}%",))
    else:
        cursor.execute("SELECT id, name, speciality, days, timings, fee FROM doctors")
        
    doctors = cursor.fetchall()
    conn.close()
    
    if not doctors:
        return "No doctors found matching the query."
    
    result = " Available Doctors:\n"
    for doc in doctors:
        result += f"- [ID: {doc[0]}] {doc[1]} ({doc[2]}) | Days: {doc[3]} | Time: {doc[4]} | Fee: PKR {doc[5]}\n"
    return result

@tool
def check_doctor_booked_slots(doctor_id: int, date: str) -> str:
    """Check booked appointments for a doctor on a specific date (Format: YYYY-MM-DD) to avoid double booking."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT appointment_time FROM appointments 
        WHERE doctor_id = ? AND appointment_date = ? AND status = 'Confirmed'
    """, (doctor_id, date))
    
    booked = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    if not booked:
        return f"All slots are currently free for Doctor ID {doctor_id} on {date}."
    return f"Already booked times for Doctor ID {doctor_id} on {date}: {', '.join(booked)}"

@tool
def book_appointment(patient_name: str, patient_phone: str, doctor_id: int, date: str, time: str) -> str:
    """Confirm and save a new patient appointment into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO appointments (patient_name, patient_phone, doctor_id, appointment_date, appointment_time)
            VALUES (?, ?, ?, ?, ?)
        """, (patient_name, patient_phone, doctor_id, date, time))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return f"✅ SUCCESS: Appointment booked! Booking Reference ID: #APT-{booking_id} for {patient_name} on {date} at {time}."
    except Exception as e:
        conn.close()
        return f"❌ Error booking appointment: {str(e)}"