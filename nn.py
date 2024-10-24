import mysql.connector
import matplotlib.pyplot as plt

# Database Connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root123",
        database="student_management"
    )

# User Management Functions
def login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Student Information Functions
def fetch_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    
    # Display students in a table-like structure
    print("******************************************************************************")
    print("\t\t\t    STUDENTS LIST ")
    print("******************************************************************************")
    print(f"{'ID':<5} {'Name':<20} {'Course':<15} {'Department':<10}")
    print("-" * 55)
    for student in students:
        print(f"{student[0]:<5} {student[1]:<20} {student[2]:<15} {student[3]:<10}")
    
    return students  # Return the list of students


def add_student(name,rollno, course,email,phone):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, roll_number, course,email,phone) VALUES (%s, %s, %s,%s, %s)", (name,rollno, course,email,phone))
    conn.commit()
    conn.close()
    print(f"Student '{name}' added successfully!")

def fetch_student_marks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT s.name, m.subject, m.marks FROM students s JOIN marks m ON s.id = m.student_id")
    marks = cursor.fetchall()
    conn.close()
    
    # Display marks in a table-like structure
    print("******************************************************************************")
    print("\t\t\t    STUDENT MARKS ")
    print("******************************************************************************")
    print(f"{'Student Name':<20} {'Subject':<15} {'Marks':<5}")
    print("-" * 45)
    for mark in marks:
        print(f"{mark[0]:<20} {mark[1]:<15} {mark[2]:<5}")

# Attendance Management Functions
def mark_attendance(student_id, status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, CURDATE(), %s)", (student_id, status))
    conn.commit()
    conn.close()

# Visualization Functions
def show_attendance_chart():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name, COUNT(a.status) 
        FROM students s 
        LEFT JOIN attendance a ON s.id = a.student_id AND a.status = 'present' 
        GROUP BY s.id
    """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No attendance data found.")
        return

    names = [x[0] for x in data]
    attendance = [x[1] if x[1] is not None else 0 for x in data]  # Handle None values

    plt.bar(names, attendance, color='blue')
    plt.xlabel('Students')
    plt.ylabel('Days Present')
    plt.title('Attendance Record')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def visualize_student_marks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT subject, marks FROM marks")
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        print("No marks data found.")
        return
    
    # Organize marks by subject
    subjects = {}
    for subject, mark in data:
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(mark)
    
    # Prepare data for boxplot
    subject_names = list(subjects.keys())
    subject_marks = [subjects[subject] for subject in subject_names]
    
    # Create the boxplot
    plt.boxplot(subject_marks, labels=subject_names, patch_artist=True)
    plt.xlabel('Subjects')
    plt.ylabel('Marks')
    plt.title('Boxplot of Student Marks by Subject')
    plt.grid(True)
    plt.show()

# Main Console Application
def main():
    while True:
        print("******************************************************************************")
        print("\t\t Welcome to the Student Management System")
        print("******************************************************************************")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        
        user = login(username, password)
        if user:
            print("Login successful!")
            print("Welcome!!!!")
            break
        else:
            print("Invalid username or password. Please try again.")

    while True:
        print("\nMain Menu")
        print("1. View Students")
        print("2. Add Student")
        print("3. Mark Attendance")
        print("4. View Attendance Chart")
        print("5. View Student Marks")
        print("6. Visualize Student Marks")
        print("7. Exit")
        print("\n")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == '1':
            fetch_students()
        
        elif choice == '2':
            
            name = input("Enter student name: ")
            rollno = input("Enter rollno: ")
            course = input("Enter course: ")
            email = input("Enter email: ")
            phone = input("Enter phone no : ")
            add_student(name,rollno, course,email,phone)
        
        elif choice == '3':
            students = fetch_students()  # Get the list of students
            print("\nMark Attendance:")
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}")
                status = input("Enter attendance (present/absent): ").strip().lower()
                if status in ['present', 'absent']:
                    mark_attendance(student[0], status)
                    print(f"Attendance marked as {status}.")
                else:
                    print("Invalid status. Please enter 'present' or 'absent'.")

        
        elif choice == '4':
            show_attendance_chart()
        
        elif choice == '5':
            fetch_student_marks()
        
        elif choice == '6':
            visualize_student_marks()
        
        elif choice == '7':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice, Please try again.")

if __name__ == "__main__":
    main()


