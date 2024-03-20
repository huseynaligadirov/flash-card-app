# language.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QListWidget
from save import DataManager
class Language:
    languages = []
    data = {}
    def __init__(self, main_data):
        self.data = main_data
        self.data_manager = DataManager()
        

    def add_language(self, language_code):
        self.languages.append(language_code)

    def remove_language(self, language_code):
        self.languages.remove(language_code)

    def list_languages(self):
        return self.languages

    def add_new_language_dialog(self, source_language_list, target_language_list):
        dialog = QDialog()
        dialog.setWindowTitle("Add Language")
        layout = QVBoxLayout(dialog)
        language_label = QLabel("Language Code:", dialog)
        language_input = QLineEdit(dialog)
        layout.addWidget(language_label)
        layout.addWidget(language_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_new_language(language_input.text(), source_language_list, target_language_list , dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()

    def add_new_language(self, language_code, source, target,  dialog):
        
        self.add_language(language_code)
        source.addItem(language_code),
        target.addItem(language_code)
        self.data['languages'].append(language_code)
        self.data_manager.saveData(self.data)
        dialog.accept()
