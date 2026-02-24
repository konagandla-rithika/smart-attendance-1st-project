import mysql.connector
from datetime import datetime

# Replace these with your database details
db = mysql.connector.connect(
    host="localhost",       # use cloud host if using cloud MySQL
    user="root",            # your MySQL username
    password="root",# your MySQL password
    database="attendance_system"  # database name
)

cursor = db.cursor()

def mark_attendance(name):
    now = datetime.now()
    date = now.date()
    time = now.time()
    
    # Check if attendance already marked today
    cursor.execute("SELECT * FROM attendance WHERE name=%s AND date=%s", (name, date))
    result = cursor.fetchone()
    
    if not result:
        cursor.execute(
            "INSERT INTO attendance (name, date, time) VALUES (%s, %s, %s)",
            (name, date, time)
        )
        db.commit()
        return f"Attendance marked for {name} at {time}"
    else:
        return f"Attendance already marked for {name} today"
