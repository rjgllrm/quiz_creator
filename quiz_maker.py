import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QRadioButton, QPushButton,
    QVBoxLayout, QMessageBox, QButtonGroup, QDialog
)
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt

class ResultDialog(QDialog):
    def __init__(self, message, gif_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Result")
        self.setFixedSize(400, 400)
        
        layout = QVBoxLayout()

        gif_label = QLabel()
        movie = QMovie(gif_path)
        gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(gif_label, alignment=Qt.AlignCenter)

        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("font-size: 21px; font-weight: bold;")
        layout.addWidget(message_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        
class FinalDialog(QDialog):
    def __init__(self, message, gif_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quiz Completed!")
        self.setFixedSize(500, 500)

        layout = QVBoxLayout()
        
        gif_label = QLabel()
        movie = QMovie(gif_path)
        gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(gif_label, alignment=Qt.AlignCenter)

        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(message_label)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

class Quiz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quiz Time!")
        self.question_data = self.load_questions()

        if not self.question_data:
            QMessageBox.critical(self, "Error", "No questions found!")
            sys.exit()

        self.remaining_questions = self.question_data.copy()
        random.shuffle(self.remaining_questions)

        self.init_ui()

     def load_questions(self):
        try:
            with open("quiz_creator_questions.txt", "r", encoding="utf-8") as file:
                content = file.read().strip().split("-" * 40)

            questions = []
            for block in content:
                lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
                if len(lines) < 6:
                    continue

                question_text = lines[0][len("Question: "):]
                options = [
                    lines[1][len("a) "):],
                    lines[2][len("b) "):],
                    lines[3][len("c) "):],
                    lines[4][len("d) "):]
                ]
                correct = lines[5][len("Correct Answer: "):].upper()

                questions.append({
                    "question": question_text,
                    "options": options,
                    "correct": correct
                })
            return questions
        except FileNotFoundError:
            return []

    def init_ui(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#f0f8ff"))
        self.setPalette(palette)

        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.question_label = QLabel()
        self.question_label.setStyleSheet("font-size: 41px; font-weight: bold; color: #4caf50;")
        self.layout.addWidget(self.question_label)

        self.radio_buttons = []
        self.button_group = QButtonGroup()
        for me in range(4):
            rb = QRadioButton()
            rb.setStyleSheet("font-size: 21px; margin: 10px;")
            self.radio_buttons.append(rb)
            self.button_group.addButton(rb, me)
            self.layout.addWidget(rb)
            
        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet("background-color: #4caf50; font-size: 21px; color: white; padding: 5px;")
        self.submit_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        self.load_random_question()

    def load_random_question(self):
        if not self.remaining_questions:
            final_dialog = FinalDialog("🎉 Quiz Finished!", "finish.gif", self)
            final_dialog.exec_()
            self.close()
            return
        self.current_question = self.remaining_questions.pop()
        self.question_label.setText(self.current_question["question"])

        pixmap = QPixmap("banner.jpg")
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(900, 900, Qt.KeepAspectRatio))
        else:
            self.image_label.clear()

        for you, option in enumerate(self.current_question["options"]):
            self.radio_buttons[you].setText(option)
            self.radio_buttons[you].setChecked(False)

    def check_answer(self):
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "Please select an answer before submitting.")
            return

        selected_option = ['A', 'B', 'C', 'D'][selected_id]
        correct_option = self.current_question['correct']

        if selected_option == correct_option:
            message = f"✅ Correct! The answer is {correct_option}."
            gif_path = "correct.gif"
        else:
            message = f"❌ Wrong! The correct answer is {correct_option}."
            gif_path = "wrong.gif"

        dialog = ResultDialog(message, gif_path, self)
        dialog.exec_()

        self.load_random_question()

def main():
    app = QApplication(sys.argv)
    quiz = Quiz()
    quiz.resize(850, 900)
    quiz.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

