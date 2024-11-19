import psycopg2
from psycopg2 import sql
from psycopg2.errors import DuplicateDatabase, DuplicateTable
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QRadioButton, QComboBox, \
    QFormLayout, QMessageBox
import re

def create_database():
    try:
        conn = psycopg2.connect(host='localhost', port=5432, user='postgres', password='1253', dbname='postgres')
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(sql.SQL("CREATE DATABASE student_database"))
        except DuplicateDatabase:
            print("Database already exists.")

        cur.close()
        conn.close()

        conn = psycopg2.connect(host='localhost', port=5432, user='postgres', password='1253',
                                dbname='student_database')
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(32),
                last_name VARCHAR(32),
                age INT,
                gender VARCHAR(16),
                region VARCHAR(32),
                phone VARCHAR(15),
                faculty VARCHAR(32),
                course VARCHAR(8)
            )
        """)
        conn.commit()

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def insert_student(first_name, last_name, age, gender, region, phone, faculty, course):
    try:
        conn = psycopg2.connect(host='localhost', port=5432, user='postgres', password='1253',
                                dbname='student_database')
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO students (first_name, last_name, age, gender, region, phone, faculty, course)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, age, gender, region, phone, faculty, course))
        conn.commit()

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


class Student(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Registration')
        self.setGeometry(300, 300, 500, 500)
        self.layout = QVBoxLayout()

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.age = QLineEdit()
        self.phone = QLineEdit()
        self.faculty = QLineEdit()

        self.gender_male = QRadioButton("Male")
        self.gender_female = QRadioButton("Female")

        self.region_combo = QComboBox()
        self.region_combo.addItems([
            "Toshkent viloyati", "Andijon viloyati", "Farg‘ona viloyati", "Namangan viloyati",
            "Samarqand viloyati", "Buxoro viloyati", "Navoiy viloyati", "Qashqadaryo viloyati",
            "Surxondaryo viloyati", "Jizzax viloyati", "Sirdaryo viloyati", "Xorazm viloyati"
        ])
        self.course_combo = QComboBox()
        self.course_combo.addItems(["1-course", "2-course", "3-course", "4-course", "5-course"])

        self.save_button = QPushButton("Save Student")
        self.save_button.clicked.connect(self.save_student)

        form_layout = QFormLayout()
        form_layout.addRow("First Name", self.first_name)
        form_layout.addRow("Last Name", self.last_name)
        form_layout.addRow("Age", self.age)
        form_layout.addRow("Gender", self.gender_male)
        form_layout.addWidget(self.gender_female)
        form_layout.addRow("Region", self.region_combo)
        form_layout.addRow("Phone", self.phone)
        form_layout.addRow("Faculty", self.faculty)
        form_layout.addRow("Course", self.course_combo)

        self.layout.addLayout(form_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_student(self):
        first_name = self.first_name.text()
        last_name = self.last_name.text()
        age = self.age.text()
        gender = "Male" if self.gender_male.isChecked() else "Female"
        region = self.region_combo.currentText()
        phone = self.phone.text()
        faculty = self.faculty.text()
        course = self.course_combo.currentText()

        if not self.is_valid_name(first_name) or not self.is_valid_name(last_name):
            self.show_error("Invalid Name or Surname")
            return
        if not self.is_valid_age(age):
            self.show_error("Invalid Age")
            return
        if not self.is_valid_phone(phone):
            self.show_error("Invalid Phone")
            return
        if not faculty:
            self.show_error("Please enter the faculty")
            return

        insert_student(first_name, last_name, age, gender, region, phone, faculty, course)
        self.show_success("Student saved successfully")

    def is_valid_name(self, name):
        return bool(re.match(r'^[A-Z][a-z]*$', name))

    def is_valid_age(self, age):
        return age.isdigit() and 10 <= int(age) <= 100

    def is_valid_phone(self, phone):
        return bool(re.match(r'^\+\d{12}$', phone))

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle('Error')
        msg.exec()

    def show_success(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle('Success')
        msg.exec()


if __name__ == '__main__':
    create_database()

    app = QApplication(sys.argv)
    window = Student()
    window.show()
    sys.exit(app.exec())
