import sys
import re
from collections import deque
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QLabel
)
from PyQt6.QtCore import QDate
import psycopg2

task_queue = deque()
task_stack = []


def get_db_connection():
    return psycopg2.connect(
        host='', #use yours
        port=5432, #use yours
        database='', #use yours
        user='', #use yours
        password='' #use yours
    )


def insert_task(title, description, deadline, time, assigned_to):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO tasks (title, description, deadline, time, assigned_to)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (title, description, deadline, time, assigned_to))
    connection.commit()

    cursor.close()
    connection.close()


class ToDoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Vazifa nomi (Title)")
        layout.addWidget(QLabel("Vazifa nomi"))
        layout.addWidget(self.title_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Vazifa tavsifi (Description)")
        layout.addWidget(QLabel("Vazifa tavsifi"))
        layout.addWidget(self.description_input)

        self.deadline_input = QLineEdit()
        self.deadline_input.setPlaceholderText("Tugash muddati (YYYY-MM-DD)")
        layout.addWidget(QLabel("Tugash muddati"))
        layout.addWidget(self.deadline_input)

        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("Vaqt (HH:MM)")
        layout.addWidget(QLabel("Vaqt"))
        layout.addWidget(self.time_input)

        self.assigned_to_input = QLineEdit()
        self.assigned_to_input.setPlaceholderText("Kimga yuklangan (Assigned To)")
        layout.addWidget(QLabel("Kimga yuklangan"))
        layout.addWidget(self.assigned_to_input)

        self.add_task_button = QPushButton("Vazifa qo'shish")
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.undo_button = QPushButton("Orqaga qaytarish (Undo)")
        self.undo_button.clicked.connect(self.undo_task)
        layout.addWidget(self.undo_button)

        self.setLayout(layout)

    def add_task(self):
        title = self.title_input.text().strip()
        description = self.description_input.text().strip()
        deadline = self.deadline_input.text().strip()
        time = self.time_input.text().strip()
        assigned_to = self.assigned_to_input.text().strip()

        if not title or len(title) > 255:
            self.show_error("Vazifa nomi bo'sh bo'lishi mumkin emas va 255 belgidan oshmasligi kerak.")
            return

        if len(description) > 500:
            self.show_error("Vazifa tavsifi 500 belgidan oshmasligi kerak.")
            return

        if not self.validate_date(deadline):
            self.show_error("Tugash muddati YYYY-MM-DD formatida bo'lishi va kelajakdagi sana bo'lishi kerak.")
            return

        if not self.validate_time(time):
            self.show_error("Vaqt HH:MM formatida va 24 soat ichida bo'lishi kerak.")
            return

        if not assigned_to or len(assigned_to) > 255 or not assigned_to.isalpha():
            self.show_error(
                "Kimga yuklangan bo'sh bo'lishi mumkin emas va faqat matndan iborat bo'lishi kerak (255 belgigacha).")
            return

        try:
            insert_task(title, description, deadline, time, assigned_to)

            task_data = (title, description, deadline, time, assigned_to)
            task_queue.append(task_data)
            task_stack.append(task_data)

            QMessageBox.information(self, "Muvaffaqiyat", "Vazifa muvaffaqiyatli qo'shildi!")
            self.clear_inputs()
        except Exception as e:
            self.show_error(f"Ma'lumotlar saqlashda xatolik yuz berdi: {str(e)}")

    def undo_task(self):
        if not task_stack:
            QMessageBox.warning(self, "Ogohlantirish", "Hech qanday vazifa topilmadi.")
            return

        last_task = task_stack.pop()
        QMessageBox.information(
            self, "Undo", f"So‘nggi qo‘shilgan vazifa (Stack LIFO):\n\n{last_task}")

    def validate_date(self, date_str):
        try:
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            return date.isValid() and date > QDate.currentDate()
        except:
            return False

    def validate_time(self, time_str):
        return re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time_str) is not None

    def show_error(self, message):
        QMessageBox.critical(self, "Xatolik", message)

    def clear_inputs(self):
        self.title_input.clear()
        self.description_input.clear()
        self.deadline_input.clear()
        self.time_input.clear()
        self.assigned_to_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec())
