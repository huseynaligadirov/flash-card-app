import sys
from PyQt5.QtWidgets import QDialogButtonBox,QLineEdit, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
import random
from save import DataManager
class Quiz():
    def __init__(self, main_data):
        super().__init__()
        self.data = main_data
        self.data_manager = DataManager()
        

    def generate_quiz(self,source, target, category ):
        dialog = QDialog()
        dialog.setWindowTitle("Quiz")
        layout = QVBoxLayout(dialog)
        self.vocab = {}
        if source in self.data['translations']:
            if target in self.data['translations'][source]:
                if category in self.data['translations'][source][target]:
                    self.vocab = self.data['translations'][source][target][category]
                else:
                    self.alert()
                    dialog.accept()
            else: 
                self.alert()
                dialog.accept()
        else: 
            self.alert()
            dialog.accept()

        self.source = source
        self.target = target
        self.category = category
        self.question_count = 10
        if(len(self.vocab) < 5):
            self.alert()
            return dialog.accept()            
        elif(len(self.vocab)>=5 and len(self.vocab) <=10):
            self.question_count = 5
        else:
            self.question_count = 10
        self.current_question = 0
        self.correct_ans = 0
        question_list = [x for x in self.vocab]
        self.mixed_questions = random.sample(question_list, self.question_count)
        self.label = QLabel()        
        self.label.setText(f"Question {self.current_question+1} - {self.mixed_questions[self.current_question]}")
        layout.addWidget(self.label)
        query_label = QLabel("Enter your answer:", dialog)
        self.answer_input = QLineEdit(dialog)
        layout.addWidget(query_label)
        layout.addWidget(self.answer_input)
        submit_button = QPushButton("Submit")
        pass_button = QPushButton("Pass")
        layout.addWidget(submit_button)
        layout.addWidget(pass_button)
        submit_button.clicked.connect(lambda: self.checkQuestion(self.mixed_questions[self.current_question], self.answer_input.text(), dialog, self.source, self.target, self.category) )

        

        

        
        dialog.exec_()
    
    def findAnswer (self, data, source, target, category, word):
        return data['translations'][source][target][category][word]
        
    def checkQuestion (self, question, answer , dialog, source, target, category):
        correct_answer = self.findAnswer(self.data, source, target, category, question)
        
        if(self.current_question < self.question_count-1):
            if(answer.lower() == correct_answer.lower()):
                self.correct_ans +=1
            else:
                pass
            self.current_question +=1
            self.Next()
        elif self.current_question == self.question_count-1:
            if(answer.lower() == self.vocab[question].lower()):
                self.correct_ans +=1
            else:
                pass            
     
            success_percent = self.correct_ans / self.question_count
            last_result = {}

            if (self.source in self.data['progress']):
                if(self.target in self.data['progress'][self.source]):
                    if(self.category in self.data['progress'][self.source][self.target]):
                        print(success_percent, self.data['progress'][self.source][self.target][self.category] )
                        last_result = self.data['progress'][self.source][self.target][self.category]
                     
            
            
            self.data['progress'][self.source] = {
                self.target: {
                    self.category: success_percent
                }
            }
            
            self.data_manager.saveData(self.data)
            
            self.dial(success_percent, last_result)
            dialog.accept()
        
        
    def Next(self):
        
            self.answer_input.setText('')
            new_question = self.mixed_questions[self.current_question]
            self.label.setText(f"Question {self.current_question+1} - {new_question}")
        
    def dial(self, succes, last):
        dialog = QDialog()
        dialog.setWindowTitle("Quiz")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        label_2 = QLabel()
        dialog.setWindowTitle("Quiz result")        
        corrects = self.question_count * succes
        
        label_2.setText(f"{corrects} correct answer out of {self.question_count}")
        
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(lambda: dialog.accept())
        
        layout.addWidget(label_2)
        layout.addWidget(close_btn)
        
        
        
        if(last):
            if(succes > last):
                label.setText('Great!! continue work with this effort.')
            elif succes == last:
                label.setText('Great!! continue work with this effort.')
            else:
                label.setText('It seems you need to work on you more.')
                
        
        
        

        layout.addWidget(label)
        dialog.exec_()
    
    def alert (self):
        
        dialog = QDialog()
        dialog.setWindowTitle("Alert")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        label.setText('There is no enough question')
        layout.addWidget(label)
        btn = QPushButton('Ok')
        btn.clicked.connect(lambda: dialog.accept())
        layout.addWidget(btn)
        dialog.exec_()
        
        



        

