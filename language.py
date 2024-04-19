# language.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QListWidget
from save import data_manager
from alert import AlertDialog
class Language:
    data = {}
    def __init__(self, main_data):
        self.data = main_data
        self.alertManager = AlertDialog()
        
    
    def add_source_language_dialog(self, sync):
        dialog = QDialog()
        dialog.setWindowTitle("Add Source Language")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel('Source Language name:'))
        word_input = QLineEdit(dialog)
        layout.addWidget(word_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_source_language(word_input.text().strip().capitalize(), dialog, sync))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()
        
    def add_source_language(self, name, dialog, sync):
        if (name in self.data['translations']):
            self.alertManager.alert(f"{name} is already exists as source language")
        elif (name == ''):
            self.alertManager.alert('Input can not be empty')
        else:
            self.data['translations'][name] = {}
            data_manager.saveData(self.data)
            sync()
            dialog.accept()
        
    def remove_source_language_modal(self, source_lang, sync):
        if not source_lang:
            return
        dialog = QDialog()
        dialog.setWindowTitle("Remove Source language")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Are you sure to remove {source_lang} from source languages?"))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.remove_source_language(source_lang, dialog, sync))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()
        
    def remove_source_language(self, source_lang, dialog, sync):
        del self.data['translations'][source_lang]
        data_manager.saveData(self.data)
        sync()
        dialog.accept()
        
    def remove_target_language_modal(self, source_lang, target_lang, sync):
        if not source_lang or not target_lang:
            return
        dialog = QDialog()
        dialog.setWindowTitle("Remove Target language")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Are you sure to remove {target_lang} from target list of {source_lang} languages?"))
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.remove_target_language(source_lang, target_lang, dialog, sync))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()
        
    def remove_target_language(self, source_lang, target_lang, dialog, sync):
        del self.data['translations'][source_lang][target_lang]
        data_manager.saveData(self.data)
        sync()
        dialog.accept()
        
        

            
    def add_target_language_dialog(self, source, setSource):
        if (not source):
            self.alertManager.alert('Source language must be selected')
            return

        dialog = QDialog()
        dialog.setWindowTitle("Add Target Language")
        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel('Target Language name:'))
        word_input = QLineEdit(dialog)
        layout.addWidget(word_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_target_language(word_input.text().strip().capitalize(), dialog, source, setSource))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()

    def add_target_language(self, name, dialog, source, setSource):
        if (name in self.data['translations'][source]):
            self.alertManager.alert(f"{name} is already exists as target language of {source}")
        elif (name == ''):
            self.alertManager.alert('Input can not be empty')
        else:
            self.data['translations'][source][name] = {}
            data_manager.saveData(self.data)
            setSource()            
            dialog.accept()