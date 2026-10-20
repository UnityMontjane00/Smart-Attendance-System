import unittest
from storage import add_student, process_attendance, fetch_attendance_records, STUDENTS_FILE, ATTENDANCE_FILE
import sqlite3
import storage

class TestAttendanceSystem(unittest.TestCase):
    
    def setUp(self):
        """Run before each test: set up a clean test database state."""
        # Point storage to a test database in memory or temporary file
        storage.DB_FILE = sqlite3.connect(":memory:") # Or a temp file
        # Re-initialize tables for the test
        storage.init_db()

    def test_add_student_success(self):
        """Test successfully registering a new student."""
        success, message = add_student("S999", "Test Student")
        self.assertTrue(success)
        self.assertIn("registered successfully", message)

    def test_add_duplicate_student(self):
        """Test that registering the same student ID twice fails."""
        add_student("S999", "Test Student")
        success, message = add_student("S999", "Duplicate Student")
        self.assertFalse(success)
        self.assertIn("already registered", message)

    def test_process_attendance_unregistered(self):
        """Test that unregistered students cannot mark attendance."""
        success, message = process_attendance("UNKNOWN_ID")
        self.assertFalse(success)
        self.assertIn("not registered", message)

    def test_process_attendance_success_and_duplicate(self):
        """Test marking attendance once successfully, and blocking a duplicate on the same day."""
        add_student("S101", "Alice")
        
        # First mark should succeed
        success1, msg1 = process_attendance("S101")
        self.assertTrue(success1)
        
        # Second mark on the same day should fail (duplicate)
        success2, msg2 = process_attendance("S101")
        self.assertFalse(success2)
        self.assertIn("Already marked", msg2)

if __name__ == "__main__":
    unittest.main()