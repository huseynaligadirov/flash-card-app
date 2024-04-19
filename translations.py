# translation.py
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QListWidget, QComboBox
from save import data_manager
from category import Category
from alert import AlertDialog
class Translations:
    translations = {}

    def __init__(self, main_data):
        self.data = main_data
        self.translations = main_data['translations']
        self.alertManager = AlertDialog()
        self.category_manager = Category(main_data)

    def remove_translation(self, index):
        del self.translations[index]

    def list_translations(self):
        return self.translations

    def add_new_translation_dialog(self, source, target, category, setTarget):
        if not source or not target:
            self.alertManager.alert('Source and target languages must be selected!')
            return
        dialog = QDialog()
        dialog.setWindowTitle("Add Translation")
        layout = QVBoxLayout(dialog)
        word_label = QLabel("Word:", dialog)
        self.word_input = QLineEdit(dialog)
        translation_label = QLabel("Translation:", dialog)
        self.translation_input = QLineEdit(dialog)
        category_label = QLabel("Category:", dialog)
        self.category_input = QLineEdit()
        self.category_input.setText(category)

        layout.addWidget(word_label)
        layout.addWidget(self.word_input)
        layout.addWidget(translation_label)
        layout.addWidget(self.translation_input)
        layout.addWidget(category_label)
        layout.addWidget(self.category_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_new_translation(source, target, self.word_input.text().strip().capitalize(), self.translation_input.text().strip().capitalize(), self.category_input.text().strip().capitalize(), dialog, setTarget))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()

    def add_new_translation(self, source, target, word, translation, category, dialog, setTarget ):        
        if not word or not translation:
            self.alertManager.alert('Input can not be empty!')
            return
        if ' | ' in word or ' | ' in translation:
            self.alertManager.alert('Pattern is not allowed!')
            return
        if category in self.data['translations'][source][target]:
            if word in self.data['translations'][source][target][category]:
                self.alertManager.alert('This word already exists')
                return
        else:
            if (category == ''):
                self.alertManager.alert('Input can not be empty')
                return
            self.category_manager.add_category(category, source, target, dialog, setTarget)
        

        self.data['translations'][source][target][category][word] = translation
        setTarget()
        data_manager.saveData(self.data)
        dialog.accept()
        
    def remove_translation_modal(self, source, target, category, word, sync):
        if not source or not target or not category or not word:
            self.alertManager.alert("Source language, target language and category must be selected to delete specific translation")
            return
        dialog = QDialog()
        dialog.setWindowTitle("Remove selected translation")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Are you sure to remove selected translation?"))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.remove_translation(source, target, category, word, dialog, sync))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()
        
    def remove_translation(self, source_lang, target_lang,category, word, dialog, sync):
        del self.data['translations'][source_lang][target_lang][category][word.split(' | ')[0]]
        data_manager.saveData(self.data)
        sync()
        dialog.accept()
        
        
            
            
        
        
        
       
        
