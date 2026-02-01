import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import csv
import os

# Set page config
st.set_page_config(page_title="Orzala Academy", page_icon="📚", layout="wide")

# Create Logo using SVG
logo_svg = """
<svg width="80" height="80" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M20 30 Q25 35 20 45 L15 35 Z" fill="#2D3E50" />
  <path d="M80 30 Q75 35 80 45 L85 35 Z" fill="#2D3E50" />
  <circle cx="50" cy="25" r="8" fill="#0EA5E9" />
  <path d="M50 35 Q40 40 35 50 Q50 55 65 50 Q60 40 50 35 Z" fill="#0EA5E9" />
  <path d="M35 60 Q45 70 65 50" stroke="#0EA5E9" stroke-width="3" fill="none" stroke-linecap="round" />
</svg>
"""

# Display logo and header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown(logo_svg, unsafe_allow_html=True)
with col2:
    st.markdown("# 📚 ORZALA ACADEMY")
    st.markdown("### Administrative Management System")

st.markdown("---")

# Initialize session state for data storage
if 'teachers' not in st.session_state:
    st.session_state.teachers = [
        {'id': 1, 'name': 'Ahmed Khan', 'subject': 'Mathematics', 'email': 'ahmed@orzala.edu', 'phone': '03001234567', 'joinDate': '2023-01-15'},
        {'id': 2, 'name': 'Fatima Ali', 'subject': 'English', 'email': 'fatima@orzala.edu', 'phone': '03009876543', 'joinDate': '2023-03-20'}
    ]

if 'students' not in st.session_state:
    st.session_state.students = [
        {'id': 1, 'name': 'Hassan Ahmed', 'rollNo': 'S001', 'class': '9A', 'gpa': 3.8, 'email': 'hassan@student.edu', 'enrollDate': '2023-04-10'},
        {'id': 2, 'name': 'Ayesha Malik', 'rollNo': 'S002', 'class': '9B', 'gpa': 3.9, 'email': 'ayesha@student.edu', 'enrollDate': '2023-04-10'},
        {'id': 3, 'name': 'Ali Raza', 'rollNo': 'S003', 'class': '9A', 'gpa': 3.5, 'email': 'ali@student.edu', 'enrollDate': '2023-04-12'}
    ]

if 'attendance' not in st.session_state:
    st.session_state.attendance = {}

if 'marks' not in st.session_state:
    st.session_state.marks = {}

# Header
st.markdown("# 📚 ORZALA ACADEMY")
st.markdown("## Administrative Management System")
st.markdown("---")

# Sidebar Navigation
st.sidebar.markdown("# 📊 Navigation")
page = st.sidebar.radio("Select Page:", 
    ["Overview", "Teachers", "Students", "Attendance", "Marks", "Analytics"])

# ============= OVERVIEW PAGE =============
if page == "Overview":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Teachers", len(st.session_state.teachers))
    
    with col2:
        st.metric("Total Students", len(st.session_state.students))
    
    with col3:
        avg_gpa = sum([s['gpa'] for s in st.session_state.students]) / len(st.session_state.students) if st.session_state.students else 0
        st.metric("Average GPA", f"{avg_gpa:.2f}")
    
    st.markdown("---")
    st.markdown("### 📈 Quick Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"✅ Total Classes: 3 (9A, 9B, 10A)")
    with col2:
        st.info(f"✅ Total Subjects: 4")

# ============= TEACHERS PAGE =============
elif page == "Teachers":
    st.markdown("# 👨‍🏫 Teachers Management")
    
    # Add teacher form
    with st.expander("➕ Add New Teacher", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Teacher Name")
            email = st.text_input("Email")
        with col2:
            subject = st.text_input("Subject")
            phone = st.text_input("Phone")
        
        joinDate = st.date_input("Join Date")
        
        if st.button("✅ Add Teacher", key="add_teacher"):
            if name and subject and email:
                new_teacher = {
                    'id': max([t['id'] for t in st.session_state.teachers], default=0) + 1,
                    'name': name,
                    'subject': subject,
                    'email': email,
                    'phone': phone,
                    'joinDate': str(joinDate)
                }
                st.session_state.teachers.append(new_teacher)
                st.success("✅ Teacher added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill all fields!")
    
    # Display teachers
    st.markdown("### 📋 All Teachers")
    if st.session_state.teachers:
        df = pd.DataFrame(st.session_state.teachers)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No teachers added yet!")

# ============= STUDENTS PAGE =============
elif page == "Students":
    st.markdown("# 👨‍🎓 Students Management")
    
    # Add student form
    with st.expander("➕ Add New Student", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student Name")
            rollNo = st.text_input("Roll Number")
            email = st.text_input("Email")
        with col2:
            class_name = st.selectbox("Class", ["9A", "9B", "10A"])
            gpa = st.number_input("GPA", min_value=0.0, max_value=4.0, step=0.1)
        
        enrollDate = st.date_input("Enrollment Date")
        
        if st.button("✅ Add Student", key="add_student"):
            if name and rollNo and email:
                new_student = {
                    'id': max([s['id'] for s in st.session_state.students], default=0) + 1,
                    'name': name,
                    'rollNo': rollNo,
                    'class': class_name,
                    'gpa': gpa,
                    'email': email,
                    'enrollDate': str(enrollDate)
                }
                st.session_state.students.append(new_student)
                st.success("✅ Student added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill all fields!")
    
    # Display students
    st.markdown("### 📋 All Students")
    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No students added yet!")

# ============= ATTENDANCE PAGE =============
elif page == "Attendance":
    st.markdown("# ✅ Attendance Sheet")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("Select Class", ["9A", "9B", "10A"])
    with col2:
        attendance_date = st.date_input("Select Date", datetime.now())
    
    # Get students in selected class
    class_students = [s for s in st.session_state.students if s['class'] == selected_class]
    
    if class_students:
        st.markdown(f"### Students in {selected_class}")
        
        attendance_data = {}
        for student in class_students:
            key = f"{attendance_date}-{selected_class}-{student['id']}"
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{student['name']}** ({student['rollNo']})")
            with col2:
                status = st.selectbox(
                    "Status",
                    ["Present", "Absent"],
                    key=f"att_{student['id']}"
                )
                attendance_data[key] = status
        
        # Save attendance
        if st.button("💾 Save Attendance"):
            st.session_state.attendance.update(attendance_data)
            st.success("✅ Attendance saved!")
        
        # Download attendance
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download as CSV"):
                csv_data = f"Roll No,Student Name,Status,Date,Class\n"
                for student in class_students:
                    key = f"{attendance_date}-{selected_class}-{student['id']}"
                    status = st.session_state.attendance.get(key, "Absent")
                    csv_data += f"{student['rollNo']},{student['name']},{status},{attendance_date},{selected_class}\n"
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"Attendance_{selected_class}_{attendance_date}.csv",
                    mime="text/csv"
                )
    else:
        st.info(f"No students in {selected_class}")

# ============= MARKS PAGE =============
elif page == "Marks":
    st.markdown("# 📝 Marks Management")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_subject = st.selectbox("Select Subject", ["Mathematics", "English", "Science", "Urdu"])
    with col2:
        marks_date = st.date_input("Select Date", datetime.now())
    
    st.markdown(f"### Enter Marks for {selected_subject}")
    
    marks_data = {}
    for student in st.session_state.students:
        key = f"{marks_date}-{selected_subject}-{student['id']}"
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{student['name']}** ({student['rollNo']})")
        with col2:
            mark = st.number_input(
                "Marks",
                min_value=0,
                max_value=100,
                key=f"marks_{student['id']}"
            )
            marks_data[key] = mark
        with col3:
            # Calculate grade
            if mark >= 80:
                grade = "A+"
            elif mark >= 70:
                grade = "A"
            elif mark >= 60:
                grade = "B"
            elif mark >= 50:
                grade = "C"
            elif mark >= 40:
                grade = "D"
            else:
                grade = "F"
            st.metric("Grade", grade)
    
    # Save marks
    if st.button("💾 Save Marks"):
        st.session_state.marks.update(marks_data)
        st.success("✅ Marks saved!")
    
    # Download marks
    if st.button("📥 Download Marks as CSV"):
        csv_data = f"Roll No,Student Name,Subject,Marks,Date\n"
        for student in st.session_state.students:
            key = f"{marks_date}-{selected_subject}-{student['id']}"
            mark = st.session_state.marks.get(key, 0)
            csv_data += f"{student['rollNo']},{student['name']},{selected_subject},{mark},{marks_date}\n"
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"Marks_{selected_subject}_{marks_date}.csv",
            mime="text/csv"
        )

# ============= ANALYTICS PAGE =============
elif page == "Analytics":
    st.markdown("# 📈 Analytics & Reports")
    
    col1, col2 = st.columns(2)
    
    # Class Distribution
    with col1:
        st.markdown("### 👥 Students by Class")
        class_data = {}
        for student in st.session_state.students:
            class_data[student['class']] = class_data.get(student['class'], 0) + 1
        
        if class_data:
            fig = px.bar(
                x=list(class_data.keys()),
                y=list(class_data.values()),
                labels={'x': 'Class', 'y': 'Count'},
                title="Student Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # GPA Distribution
    with col2:
        st.markdown("### 📊 GPA Distribution")
        gpa_ranges = {
            '3.5-4.0': len([s for s in st.session_state.students if s['gpa'] >= 3.5]),
            '3.0-3.49': len([s for s in st.session_state.students if 3.0 <= s['gpa'] < 3.5]),
            'Below 3.0': len([s for s in st.session_state.students if s['gpa'] < 3.0])
        }
        
        fig = px.pie(
            values=list(gpa_ranges.values()),
            names=list(gpa_ranges.keys()),
            title="GPA Ranges"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Statistics
    st.markdown("---")
    st.markdown("### 📋 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Teachers", len(st.session_state.teachers))
    with col2:
        st.metric("Total Students", len(st.session_state.students))
    with col3:
        avg_gpa = sum([s['gpa'] for s in st.session_state.students]) / len(st.session_state.students) if st.session_state.students else 0
        st.metric("Average GPA", f"{avg_gpa:.2f}")
    with col4:
        ratio = len(st.session_state.students) / len(st.session_state.teachers) if st.session_state.teachers else 0
        st.metric("Student-Teacher Ratio", f"{ratio:.1f}")