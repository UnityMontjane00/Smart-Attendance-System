import streamlit as st
from storage import (
    fetch_students, 
    add_student, 
    process_attendance, 
    fetch_attendance_records, 
    get_attendance_summary
)
from ai_helper import generate_ai_response
# Page configuration
st.set_page_config(page_title="Smart Attendance System", page_icon="🏫", layout="centered")

st.title("Smart Attendance System")
st.write("Manage students, mark daily attendance, and view reports through a clean web dashboard.")

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigation Menu", 
    ["Mark Attendance", "Register Student", "View Attendance Logs", "Student Roster", "Summary Report", "🤖 AI Assistant"]
)
# --- 1. MARK ATTENDANCE ---
if menu == "Mark Attendance":
    st.header("Mark Daily Attendance")
    
    students = fetch_students()
    if not students:
        st.warning("No registered students found! Please register students first.")
    else:
        student_options = {f"{s['ID']} - {s['Name']}": s['ID'] for s in students}
        selected_display = st.selectbox("Select Student", list(student_options.keys()))
        
        if st.button("Submit Attendance", type="primary"):
            selected_id = student_options[selected_display]
            success, message = process_attendance(selected_id)
            if success:
                st.success(message)
            else:
                st.error(message)

# --- 2. REGISTER STUDENT ---
elif menu == "Register Student":
    st.header("📝 Register a New Student")
    
    with st.form("registration_form"):
        s_id = st.text_input("Student ID (e.g., S105)")
        name = st.text_input("Student Full Name")
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            success, message = add_student(s_id, name)
            if success:
                st.success(message)
            else:
                st.error(message)
# --- 3. VIEW ATTENDANCE LOGS ---
elif menu == "View Attendance Logs":
    st.header("📋 Raw Attendance Logs")
    records = fetch_attendance_records()
    
    if not records:
        st.info("No attendance records found yet.")
    else:
        st.dataframe(records, use_container_width=True)

# --- 4. STUDENT ROSTER ---
elif menu == "Student Roster":
    st.header("🎓 Enrolled Students Roster")
    students = fetch_students() 
    if not students:
        st.info("No students registered yet.")
    else:
        st.dataframe(students, use_container_width=True)

# --- 5. SUMMARY REPORT ---
elif menu == "Summary Report":
    st.header("📊 Attendance Summary Report")
    summary = get_attendance_summary()
    
    if not summary:
        st.info("No summary data available.")
    else:
        st.dataframe(summary, use_container_width=True)
 
# --- 6. AI ASSISTANT ---
elif menu == "🤖 AI Assistant":
    st.header("🤖 Smart Attendance AI Assistant")
    st.write("Ask questions about your students, attendance records, or summary reports in plain English!")

    # Initialize chat history in Streamlit session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render all chat history on page rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user chat input
    if prompt := st.chat_input("Ask something about your attendance system..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing database..."):
                response = generate_ai_response(prompt)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})