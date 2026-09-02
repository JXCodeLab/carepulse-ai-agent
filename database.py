import sqlite3

def init_db():
    conn = sqlite3.connect("clinic.db")
    cursor = conn.cursor()

    # 1. Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        speciality TEXT NOT NULL,
        days TEXT NOT NULL,
        timings TEXT NOT NULL,
        fee INTEGER NOT NULL
    )
    """)

    # 2. Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        patient_phone TEXT,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
    """)

    # 3. Add Sample Doctors (Agar table khali ho)
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        sample_doctors = [
            ("Dr. Bilal Khan", "Dentist", "Monday, Wednesday, Friday", "03:00 PM - 07:00 PM", 2000),
            ("Dr. Ayesha Noor", "Dermatologist (Skin)", "Tuesday, Thursday, Saturday", "04:00 PM - 08:00 PM", 2500),
            ("Dr. Hamza Tariq", "General Physician", "Monday, Tuesday, Wednesday, Thursday, Friday", "10:00 AM - 02:00 PM", 1500)
        ]
        cursor.executemany("""
        INSERT INTO doctors (name, speciality, days, timings, fee)
        VALUES (?, ?, ?, ?, ?)
        """, sample_doctors)

    conn.commit()
    conn.close()
    print(" Database created successfully with sample clinic data!")

if __name__ == "__main__":
    init_db()