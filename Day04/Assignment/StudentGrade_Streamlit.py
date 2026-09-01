import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student Grade Dashboard",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS - Colorful Dashboard
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #4B0082;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #555555;
    margin-bottom: 30px;
}

.student-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}

.grade-a {
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.grade-b {
    background-color: #cce5ff;
    color: #004085;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.grade-c {
    background-color: #fff3cd;
    color: #856404;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.grade-d {
    background-color: #ffe5b4;
    color: #8a4b08;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

.grade-e {
    background-color: #f8d7da;
    color: #721c24;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Grade Calculation Function
# --------------------------------------------------

def calculate_grade(mark):

    if mark >= 90:
        return "A"

    elif mark >= 80:
        return "B"

    elif mark >= 70:
        return "C"

    elif mark >= 60:
        return "D"

    else:
        return "E"


# --------------------------------------------------
# Application Title
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎓 Student Grade Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Enter student marks and calculate subject-wise and overall grades</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Student Name
# --------------------------------------------------

st.subheader("👨‍🎓 Student Information")

student_name = st.text_input(
    "Enter Student Name:",
    placeholder="Example: Saran"
)


# --------------------------------------------------
# Subject Marks
# --------------------------------------------------

st.subheader("📝 Enter Subject Marks")

subjects = [
    "English",
    "Tamil",
    "Mathematics",
    "Social",
    "Science"
]

marks = {}

col1, col2 = st.columns(2)

with col1:

    marks["English"] = st.number_input(
        "English",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    marks["Tamil"] = st.number_input(
        "Tamil",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    marks["Mathematics"] = st.number_input(
        "Mathematics",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )


with col2:

    marks["Social"] = st.number_input(
        "Social",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    marks["Science"] = st.number_input(
        "Science",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )


# --------------------------------------------------
# Calculate Button
# --------------------------------------------------

if st.button("🎯 Calculate Grade", use_container_width=True):

    if student_name.strip() == "":
        st.warning("⚠️ Please enter the Student Name.")

    else:

        # Calculate individual subject grades
        grades = {}

        for subject in subjects:
            grades[subject] = calculate_grade(marks[subject])

        # Calculate total and average
        total_marks = sum(marks.values())

        average = total_marks / len(subjects)

        overall_grade = calculate_grade(average)

        # --------------------------------------------------
        # Student Information
        # --------------------------------------------------

        st.markdown(
            f"""
            <div class="student-card">
                <h2>👨‍🎓 {student_name}</h2>
                <p>Student Grade Report</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --------------------------------------------------
        # Overall Result
        # --------------------------------------------------

        st.subheader("🏆 Overall Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Marks",
                f"{total_marks:.0f} / 500"
            )

        with col2:
            st.metric(
                "Overall Average",
                f"{average:.2f}%"
            )

        with col3:
            st.metric(
                "Overall Grade",
                overall_grade
            )

        # --------------------------------------------------
        # Subject-wise Results
        # --------------------------------------------------

        st.subheader("📚 Subject-wise Results")

        result_data = []

        for subject in subjects:

            result_data.append({
                "Subject": subject,
                "Mark": marks[subject],
                "Percentage": marks[subject],
                "Grade": grades[subject]
            })

        df = pd.DataFrame(result_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------
        # Subject-wise Percentage Chart
        # --------------------------------------------------

        st.subheader("📊 Subject-wise Mark Percentage")

        chart_data = df.set_index("Subject")["Percentage"]

        st.bar_chart(chart_data)

        # --------------------------------------------------
        # Overall Grade Display
        # --------------------------------------------------

        grade_class = f"grade-{overall_grade.lower()}"

        st.markdown(
            f"""
            <div class="{grade_class}">
                Overall Grade: {overall_grade}
                <br>
                Average: {average:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        # --------------------------------------------------
        # Congratulations
        # --------------------------------------------------

        if overall_grade == "A":
            st.balloons()
            st.success(
                f"🎉 Congratulations {student_name}! Excellent performance!"
            )

        elif overall_grade == "B":
            st.success(
                f"👏 Well done {student_name}! Good performance!"
            )

        elif overall_grade == "C":
            st.info(
                f"👍 Good effort {student_name}! Keep improving!"
            )

        elif overall_grade == "D":
            st.warning(
                f"📖 {student_name}, you can improve with more practice."
            )

        else:
            st.error(
                f"💪 {student_name}, don't give up. Keep working hard!"
            )