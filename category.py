from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QListWidget
from save import data_manager
from alert import AlertDialog
class Category:    
    def __init__(self, main_data):
        self.data = main_data
        self.alertManager = AlertDialog()

    def add_category_modal(self, source, target, setTarget):
        if not source or not target:
            self.alertManager.alert('Source and Target languages must be selected!')
            return
        dialog = QDialog()
        dialog.setWindowTitle("Add Category")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel('Category name:'))
        word_input = QLineEdit(dialog)
        layout.addWidget(word_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_category(word_input.text().strip().capitalize(),source, target, dialog, setTarget))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()

    def add_category(self, name, source, target, dialog, setTarget):
        if name in self.data['translations'][source][target]:
            self.alertManager.alert(f"{name} is already exists as category of {source}-{target} pair")
        elif (name == ''):
            self.alertManager.alert('Input can not be empty')
        else:
            self.data['translations'][source][target][name] = {}
            data_manager.saveData(self.data)
            setTarget()
            dialog.accept()
            
    def remove_category_modal(self, source, target, category, sync):
        if not source or not target or not category: 
            return
        dialog = QDialog()
        dialog.setWindowTitle("Remove Target language")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Are you sure to remove {category} category of {source}-{target} pair?"))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.remove_category(source, target, category, dialog, sync))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()
        
    def remove_category(self, source_lang, target_lang,category, dialog, sync):
        del self.data['translations'][source_lang][target_lang][category]
        data_manager.saveData(self.data)
        sync()
        dialog.accept()