from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class AlertDialog(QDialog):
    def alert(self, message):
        dialog = QDialog()
        dialog.setWindowTitle("Quiz")
        layout = QVBoxLayout(dialog)
        label = QLabel()
        label_2 = QLabel()
        dialog.setWindowTitle("Quiz result")                
        label_2.setText(message) 
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(lambda: dialog.accept())       
        layout.addWidget(label_2)
        layout.addWidget(close_btn)        
        layout.addWidget(label)
        dialog.exec_()
