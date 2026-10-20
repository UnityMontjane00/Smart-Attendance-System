from storage import fetch_students, fetch_attendance_records, get_attendance_summary

def generate_ai_response(prompt: str) -> str:
    """
    Analyzes the user's prompt using keyword matching, 
    pulls data from storage, and generates a natural language response.
    """
    clean_prompt = prompt.lower()

    # Rule 1: Asking about students or roster
    if "student" in clean_prompt or "who" in clean_prompt and "registered" in clean_prompt:
        students = fetch_students()
        if not students:
            return "There are currently no students registered in the system."
        
        student_list = "\n".join([f"- **{s['Name']}** (ID: `{s['ID']}`)" for s in students])
        return f"Here are the registered students:\n\n{student_list}"

    # Rule 2: Asking about attendance summary or stats
    elif "summary" in clean_prompt or "how many" in clean_prompt or "attendance" in clean_prompt or "stats" in clean_prompt:
        summary = get_attendance_summary()
        if not summary:
            return "No attendance summary data is available yet."
        
        report = "\n".join([
            f"- **{row['Name']}** ({row['ID']}): **{row['TotalAttended']}** days attended" 
            for row in summary
        ])
        return f"Here is the current attendance summary:\n\n{report}"

    # Rule 3: Asking about logs / history
    elif "log" in clean_prompt or "record" in clean_prompt or "history" in clean_prompt:
        records = fetch_attendance_records()
        if not records:
            return "No attendance records have been logged yet."
        
        return f"There are a total of **{len(records)}** attendance check-ins recorded in the database."

    # Fallback response for unhandled prompts
    else:
        return (
            f"I understand you're asking about: *'{prompt}'*. "
            "Try asking me things like 'Show registered students', 'Give me the attendance summary', or 'Show attendance logs'!"
        )