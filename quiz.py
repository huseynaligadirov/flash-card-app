import sys
from PyQt5.QtWidgets import QDialogButtonBox,QLineEdit, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
import random
from save import data_manager
from alert import AlertDialog

class Quiz():
    def __init__(self, main_data):
        super().__init__()
        self.data = main_data
        self.alertManager = AlertDialog()

    def generate_quiz(self, source, target, category ):
        if not source or not target:
            self.alertManager.alert('Source and target languages must be selected to start quiz!')
            return
        dialog = QDialog()
        dialog.setWindowTitle("Quiz")
        layout = QVBoxLayout(dialog)
        self.vocab = {}
        if category in self.data['translations'][source][target]:
            self.vocab = self.data['translations'][source][target][category]
        else:
            self.vocab = {k: v for d in self.data['translations'][source][target] for k, v in self.data['translations'][source][target][d].items()}

        self.source = source
        self.target = target
        self.category = category
        self.question_count = 10
        if(len(self.vocab) < 5):
            self.alertManager.alert('There is no enough question')
            return
        elif(len(self.vocab)>=5 and len(self.vocab) <=10):
            self.question_count = len(self.vocab)
        self.current_question = 0
        self.correct_ans = 0
        self.mixed_questions = random.sample(list(self.vocab.keys()), self.question_count)
        self.label = QLabel()
        self.answer_input = QLineEdit(dialog)
        self.Next()
        layout.addWidget(self.label)
        query_label = QLabel("Enter your answer:", dialog)
        layout.addWidget(query_label)
        layout.addWidget(self.answer_input)
        submit_button = QPushButton("Submit")
        layout.addWidget(submit_button)
        submit_button.clicked.connect(lambda: self.checkQuestion(self.mixed_questions[self.current_question-1], self.answer_input.text().strip().capitalize(), dialog) )
        dialog.exec_()

    def findAnswer (self, word):
        return self.vocab[word].strip().capitalize()

    def checkQuestion (self, question, answer, dialog):
        correct_answer = self.findAnswer(question)
        text = 'Your answer is wrong ❌'
        if(answer == correct_answer):
            self.correct_ans += 1
            text = 'Your answer is correct ✅'
        else:
            text += f'\nThe correct answer is {correct_answer}'
        self.alertManager.alert(text)
        if(self.current_question == self.question_count):
            success_percent = round(100 * self.correct_ans / self.question_count)
            last_result = None
            if (self.source in self.data['progress']):
                if(self.target in self.data['progress'][self.source]):
                    if(self.category in self.data['progress'][self.source][self.target]):
                        last_result = self.data['progress'][self.source][self.target][self.category]
                    self.data['progress'][self.source][self.target][self.category] = success_percent
                else:
                    self.data['progress'][self.source][self.target] = {
                        self.category: success_percent
                    }
            else:
                self.data['progress'][self.source] = {
                    self.target: {
                        self.category: success_percent
                    }
                }

            data_manager.saveData(self.data)
            self.dial(success_percent, last_result)
            dialog.accept()

        else:
            self.Next()

    def Next(self):
        self.answer_input.setText('')
        new_question = self.mixed_questions[self.current_question]
        self.current_question += 1
        self.label.setText(f"Question {self.current_question} - {new_question}")

    def dial(self, succes, last):
        dialog = QDialog()
        dialog.setWindowTitle("Quiz")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        label_2 = QLabel()
        dialog.setWindowTitle("Quiz results")
        corrects = succes
        result_text = f"You have answered {corrects}%  of all questions correctly"
        if last:
            result_text += f" compared to previous result of {last}% on this category"
        label_2.setText(result_text)
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(lambda: dialog.accept())
        layout.addWidget(label_2)
        layout.addWidget(close_btn)
        if(last):
            if(succes > last):
                label.setText('Great job!!! Don\'t lose the peace.')
            elif succes == last:
                label.setText('Not bad) continue at this rate, and you will succeed.')
            else:
                label.setText('It seems that you need to study harder.')
        layout.addWidget(label)
        dialog.exec_()