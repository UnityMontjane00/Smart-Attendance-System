# Import our business logic functions from the storage module
from storage import (
    process_attendance, 
    fetch_attendance_records, 
    add_student, 
    fetch_students,
    get_attendance_summary  
)
def show_menu():
    print("\n" + "=" * 50)
    print("                    SMART ATTENDANCE SYSTEM")
    print("=" * 50)
    print("1. Mark Attendance")
    print("2. View Attendance Records")
    print("3. Register New Student")
    print("4. View Registered Students")
    print("5. View Attendance Summary Report")
    print("6. Exit")
    print("=" * 50)

def handle_mark_attendance():
    student_id = input("Enter Student ID: ")
    success, message = process_attendance(student_id)
    
    if success:
        print(f"\n[SUCCESS] {message}")
    else:
        print(f"\n[ERROR] {message}")


def handle_view_records():
    records = fetch_attendance_records()
    
    if not records:
        print("\nNo attendance records found!")
        return

    print("\nAttendance Records:")
    print(f"{'ID':<10} {'Date':<12} {'Time':<10}")
    print("-" * 32)
    for row in records:
        print(f"{row['ID']:<10} {row['Date']:<12} {row['Time']:<10}")


def handle_register_student():
    student_id = input("Enter New Student ID (e.g., S104): ")
    name = input("Enter Student Full Name: ")
    
    success, message = add_student(student_id, name)
    if success:
        print(f"\n[SUCCESS] {message}")
    else:
        print(f"\n[ERROR] {message}")


def handle_view_students():
    students = fetch_students()
    
    if not students:
        print("\nNo registered students found!")
        return

    print("\nRegistered Students Roster:")
    print(f"{'ID':<10} {'Name':<25}")
    print("-" * 35)
    for student in students:
        print(f"{student['ID']:<10} {student['Name']:<25}")


def handle_attendance_report():
    """Handles formatting and displaying the attendance summary report."""
    summary = get_attendance_summary()
    
    if not summary:
        print("\nNo summary data available! (Check if students are registered)")
        return

    print("\nAttendance Summary Report:")
    print(f"{'ID':<10} {'Name':<25} {'Days Attended':<15}")
    print("-" * 52)
    for row in summary:
        print(f"{row['ID']:<10} {row['Name']:<25} {row['TotalAttended']:<15}")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-6): ").strip()
        
        if choice == "1":
            handle_mark_attendance()
        elif choice == "2":
            handle_view_records()
        elif choice == "3":
            handle_register_student()
        elif choice == "4":
            handle_view_students()
        elif choice == "5":
            handle_attendance_report()
        elif choice == "6":
            print("\nExiting... Bye!")
            break
        else:
            print("\nInvalid choice! Please select between 1 and 6.")

if __name__ == "__main__":
    main()