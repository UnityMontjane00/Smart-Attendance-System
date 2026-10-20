import sqlite3
from datetime import datetime
from pathlib import Path

DB_FILE = Path("attendance.db")
def get_connection():
    """Helper to establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    # This row_factory allows us to access columns by name (like dictionaries)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                date TEXT,
                time TEXT,
                FOREIGN KEY (student_id) REFERENCES students(id)
            )
        """)
        conn.commit()

# Automatically initialize the database when storage.py is imported
init_db()
 
def add_student(student_id: str, name: str) -> tuple[bool, str]:
    """Registers a new student in the SQLite database."""
    clean_id = student_id.strip()
    clean_name = name.strip()

    if not clean_id or not clean_name:
        return False, "Student ID and Name cannot be empty!"

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO students (id, name) VALUES (?, ?)", 
                (clean_id, clean_name)
            )
            conn.commit()
        return True, f"Student '{clean_name}' ({clean_id}) registered successfully!"
    except sqlite3.IntegrityError:
        return False, f"Student ID '{clean_id}' is already registered!"


def fetch_students() -> list[dict]:
    """Retrieves all registered students as a list of dictionaries."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT id AS ID, name AS Name FROM students")
        # Convert sqlite3.Row objects to standard Python dictionaries
        return [dict(row) for row in cursor.fetchall()]


def is_valid_student(student_id: str) -> bool:
    """Checks if a student ID exists in the database roster."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT 1 FROM students WHERE id = ?", (student_id,))
        return cursor.fetchone() is not None


def process_attendance(student_id: str) -> tuple[bool, str]:
    """Validates student, checks for daily duplicates, and saves to SQLite."""
    clean_id = student_id.strip()
    if not clean_id:
        return False, "Invalid Student ID! ID cannot be empty."

    if not is_valid_student(clean_id):
        return False, f"Student ID '{clean_id}' is not registered in the system!"

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    with get_connection() as conn:
        # Check for daily duplicates using SQL
        cursor = conn.execute(
            "SELECT 1 FROM attendance WHERE student_id = ? AND date = ?", 
            (clean_id, date_str)
        )
        if cursor.fetchone():
            return False, "Already marked attendance for today!"

        # Insert attendance record
        conn.execute(
            "INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)",
            (clean_id, date_str, time_str)
        )
        conn.commit()

    return True, "Attendance marked successfully!"

def fetch_attendance_records() -> list[dict]:
    """Retrieves all attendance logs from the database."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT student_id AS ID, date AS Date, time AS Time FROM attendance"
        )
        return [dict(row) for row in cursor.fetchall()]


def get_attendance_summary() -> list[dict]:
    """Calculates attendance summary counts using an SQL JOIN query."""
    with get_connection() as conn:
        query = """
            SELECT 
                s.id AS ID, 
                s.name AS Name, 
                COUNT(a.id) AS TotalAttended
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id
            GROUP BY s.id, s.name
        """
        cursor = conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]