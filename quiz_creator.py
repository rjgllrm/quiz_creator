import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QComboBox, QMessageBox
)

class Questions(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Quiz Creator")
        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("Enter the question here...")

        self.option_inputs = []
        for label in ['A', 'B', 'C', 'D']:
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Option {label}")
            self.option_inputs.append(input_field)

        self.correct_input = QComboBox()
        self.correct_input.addItems(['A', 'B', 'C', 'D'])

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.submit_question)
        self.save_button.setStyleSheet("background-color: #66bb6a; color: white; padding: 8px;")

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setStyleSheet("background-color: #a5d6a7; padding: 6px;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.question_input)
        for input_field in self.option_inputs:
            layout.addWidget(input_field)
        layout.addWidget(self.correct_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.exit_button)
        self.setLayout(layout)

    def submit_question(self):
        question = self.question_input.toPlainText().strip()
        options = [field.text().strip() for field in self.option_inputs]
        correct = self.correct_input.currentText()

        if not question or not all(options):
           QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")
           return

        data = (
            f"Question: {question}\n"
            f"a) {options[0]}\n"
            f"b) {options[1]}\n"
            f"c) {options[2]}\n"
            f"d) {options[3]}\n"
            f"Correct Answer: {correct}\n"
            f"{'-'*40}\n"
        )

        with open("quiz_creator_questions.txt", "a", encoding="utf-8") as file:
        file.write(data)

        QMessageBox.information(self, "Saved", "Question saved!")
        self.clear_fields()

    def clear_fields(self):
        self.question_input.clear()
        for field in self.option_inputs:
            field.clear()
        self.correct_input.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = Questions()
    window.resize(400, 400)
    window.show()
    sys.exit(app.exec_())

main()

