import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QLabel, QDialog, QDialogButtonBox, QHBoxLayout, QComboBox
import json
import os
from language import Language
from save import DataManager
from category import Category
from translations import Translations

    
    
class MainWindow(QMainWindow):
    main_data = {
        "categories": [],
        "languages": [],
        "translations": {}
    }
    
    filtered_translations = {}
    def __init__(self):
        super().__init__()
        
        file_name = 'files/data.json'  
        def createFile ():
            with open('files/data.json', 'w') as json_file:
                json.dump(self.main_data, json_file)

        if os.path.exists(file_name):      
            try:
                with open(file_name, 'r') as json_file:
                    self.main_data = json.load(json_file)
            except:
                createFile()
        else:
                createFile()              
                
        #main window and layouts 
        self.setWindowTitle("Flash Card Language Learning Program")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)
        
        #functional classes
        self.language_manager = Language(self.main_data)
        self.category_manager = Category(self.main_data)
        self.translation_manager = Translations(self.main_data)
        
        #source language        
        self.source_language_label = QLabel("Source languages:")
        self.source_language_list = QListWidget()
        self.left_layout.addWidget(self.source_language_label)
        self.left_layout.addWidget(self.source_language_list)
        
        #source language    
        self.target_language_label = QLabel("Target languages:")
        self.target_language_list = QListWidget()
        self.left_layout.addWidget(self.target_language_label)
        self.left_layout.addWidget(self.target_language_list)
        
        #category
        self.category_label = QLabel("Categories:")
        self.category_list = QListWidget()
        self.left_layout.addWidget(self.category_label)
        self.left_layout.addWidget(self.category_list)
        
        #translations
        self.translations_label = QLabel("Translations:")
        self.translations_list = QListWidget()
        self.right_layout.addWidget(self.translations_label)
        self.right_layout.addWidget(self.translations_list)
        
        #buttons
        self.add_language_button = QPushButton("Add Language")
        self.left_layout.addWidget(self.add_language_button)
        
        self.remove_language_button = QPushButton("Remove Language")        
        self.left_layout.addWidget(self.remove_language_button)
        
        self.add_translation_button = QPushButton("Add Translation")
        self.right_layout.addWidget(self.add_translation_button)
        
        self.add_category_button = QPushButton("Add Category")
        self.right_layout.addWidget(self.add_category_button)         
        
        self.quiz_button = QPushButton("Start Quiz")

        #language_load
        self.saved_langs = self.main_data['languages']
        self.source_language_list.addItems(self.saved_langs)
        self.target_language_list.addItems(self.saved_langs)
        
        #category_load
        self.saved_categories = self.main_data['categories']
        self.category_list.addItems(self.saved_categories)
        
        #translation load       
        self.syncTranslations(self.main_data['translations'])
        
        #click events
        self.add_language_button.clicked.connect(lambda: self.language_manager.add_new_language_dialog(self.source_language_list, self.target_language_list))
        self.add_category_button.clicked.connect(lambda: self.category_manager.add_new_category_dialog(self.category_list))
        self.add_translation_button.clicked.connect(lambda: self.translation_manager.add_new_translation_dialog(self.translations_list) )
        
        self.source_language_list.itemClicked.connect(lambda: self.filter_for_source())
    
    def filter_for_source(self):
        current = self.source_language_list.currentItem().text()
        
        if current in self.main_data['translations']:
            self.filtered_translations[current] = self.main_data['translations'][current]
            self.syncTranslations(self.filtered_translations)
        else:
            self.filtered_translations = {}
            self.translations_list.clear()
            
    def filter_for_target(self):
        current = self.target_language_list.currentItem().text()  
    def syncTranslations(self, loaded_list):
        self.translations_list.clear()
        self.filtered_translations = {}
        for source in loaded_list:
            for target in loaded_list[source]:
                for categ in loaded_list[source][target]:
                    for word in loaded_list[source][target][categ]:
                        self.translations_list.addItem(f"{word} - {loaded_list[source][target][categ][word]}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  
