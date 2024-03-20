# translation.py
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QListWidget, QComboBox
from save import DataManager
class Translations:
    translations = {}
    
    def __init__(self, main_data):
        self.data = main_data
        self.translations = main_data['translations']
        self.data_manager = DataManager()

    def add_translation(self, translation):
        self.translations.append(translation)
        
    def save_to_file(self):
        with open('trans.json', 'w') as file:
            json.dump(self.translations, 'trans.json')
                
    def remove_translation(self, index):
        del self.translations[index]

    def list_translations(self):
        return self.translations

    def add_new_translation_dialog(self, translations_list):
        dialog = QDialog()
        dialog.setWindowTitle("Add Translation")
        layout = QVBoxLayout(dialog)
        word_label = QLabel("Word:", dialog)
        self.word_input = QLineEdit(dialog)
        translation_label = QLabel("Translation:", dialog)
        self.translation_input = QLineEdit(dialog)
        source_language_label = QLabel("Source Language:", dialog)
        self.source_language_input = QComboBox(dialog)
        self.source_language_input.addItems(self.data['languages'])
        target_language_label = QLabel("Target Language:", dialog)
        self.target_language_input = QComboBox(dialog)
        self.target_language_input.addItems(self.data['languages'])
        category_label = QLabel("Category:", dialog)
        self.category_input = QComboBox(dialog)
        self.category_input.addItems(self.data['categories'])

        layout.addWidget(word_label)
        layout.addWidget(self.word_input)
        layout.addWidget(translation_label)
        layout.addWidget(self.translation_input)
        layout.addWidget(source_language_label)
        layout.addWidget(self.source_language_input)
        layout.addWidget(target_language_label)
        layout.addWidget(self.target_language_input)
        layout.addWidget(category_label)
        layout.addWidget(self.category_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_new_translation(translations_list, dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()

    def add_new_translation(self, translations_list, dialog):
        word = self.word_input.text()
        translation = self.translation_input.text()
        source_language = self.source_language_input.currentText()
        target_language = self.target_language_input.currentText()
        category = self.category_input.currentText()

        translation_data = {
            target_language: {
                category: {
                    word: translation
                }
            }
        }
        
               
        if source_language in self.translations: 
            pass
        else:
            self.translations[source_language] = {}     
        
        
        if target_language in self.translations[source_language]:
            if category in self.translations[source_language][target_language]:
                if word in self.translations[source_language][target_language][category]:
                    pass
                else:
                    self.translations[source_language][target_language][category][word] = translation
                    translations_list.addItem(f"{word} - {translation}")
            else:
                self.translations[source_language][target_language][category] = translation_data[target_language][category]
                translations_list.addItem(f"{word} - {translation}")
                
        else:
            self.translations[source_language] = translation_data
            translations_list.addItem(f"{word} - {translation}")
            
        print(self.translations)
        self.data['translations'] = self.translations
        self.data_manager.saveData(self.data)
        dialog.accept()
        
        
       
        
