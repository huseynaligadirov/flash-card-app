import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout , QMainWindow, QToolButton, QVBoxLayout, QWidget, QPushButton, QListWidget, QLabel, QDialog, QDialogButtonBox, QHBoxLayout, QComboBox
from language import Language
from save import data_manager
from category import Category
from translations import Translations
from quiz import Quiz

class MainWindow(QMainWindow):
    main_data = {}
    filtered_translations = {}
    def __init__(self):
        super().__init__()
        self.selected_source = ''
        self.selected_target = ''
        self.selected_category = ''
        self.selected_translation=''
        self.main_data = data_manager.init()
        self.language_manager = Language(self.main_data)    
        self.category_manager = Category(self.main_data)
        self.quiz_manager = Quiz(self.main_data)
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
        self.add_language_button = QToolButton()
        self.add_language_button.setText("➕")        
        self.source_language_list = QListWidget()
        self.remove_language_button = QToolButton()
        self.remove_language_button.setText("➖")
        self.source_language_layout = QHBoxLayout()
        self.source_language_layout.addWidget(self.source_language_label)
        self.source_language_list = QListWidget()
        self.source_language_layout.addWidget(self.add_language_button)
        self.source_language_layout.addWidget(self.remove_language_button)
        self.left_layout.addLayout(self.source_language_layout)
        self.left_layout.addWidget(self.source_language_list)
        self.sync_sources()  
        #target language 
        self.target_language_label = QLabel("Target languages:")
        self.add_target_language = QToolButton()
        self.add_target_language.setText("➕")        
        self.target_language_list = QListWidget()
        self.target_language_layout = QHBoxLayout()
        self.target_language_layout.addWidget(self.target_language_label)
        self.target_language_layout.addWidget(self.add_target_language)
        self.remove_target_language_button = QToolButton()
        self.remove_target_language_button.setText("➖")
        self.target_language_layout.addWidget(self.remove_target_language_button)
        self.left_layout.addLayout(self.target_language_layout)
        self.left_layout.addWidget(self.target_language_list)  
        #category
        self.category_label = QLabel('Categories:')
        self.add_category = QToolButton()
        self.add_category.setText('➕')       
        self.category_list = QListWidget() 
        self.category_layout = QHBoxLayout()
        self.category_layout.addWidget(self.category_label)
        self.remove_category_button = QToolButton()
        self.remove_category_button.setText("➖")
        self.reset_filter_by_category = QToolButton()
        self.reset_filter_by_category.setText('🔁')      
        self.category_layout.addWidget(self.add_category)
        self.category_layout.addWidget(self.remove_category_button)
        self.category_layout.addWidget(self.reset_filter_by_category)  
        self.left_layout.addLayout(self.category_layout)
        self.left_layout.addWidget(self.category_list)  
        #translations
        self.translation_layout = QHBoxLayout()
        self.translations_label = QLabel("Translations:")
        self.translations_list = QListWidget()       
        self.add_translation_button = QToolButton()
        self.add_translation_button.setText('➕')       
        self.remove_translation_button = QToolButton()
        self.remove_translation_button.setText("➖")      
        self.translation_layout.addWidget(self.translations_label)
        self.translation_layout.addWidget(self.add_translation_button)
        self.translation_layout.addWidget(self.remove_translation_button)
        self.right_layout.addLayout(self.translation_layout)
        self.right_layout.addWidget(self.translations_list)  
        self.quiz_button = QPushButton("Start Quiz")
        self.right_layout.addWidget(self.quiz_button)


        #click events
        self.source_language_list.itemClicked.connect(self.setSource)
        self.target_language_list.itemClicked.connect(self.setTarget)
        self.translations_list.itemClicked.connect(self.setTranslation)
        self.category_list.itemClicked.connect(self.setCategory)
        self.add_language_button.clicked.connect(lambda: self.language_manager.add_source_language_dialog(self.sync_sources))
        self.add_target_language.clicked.connect(lambda: self.language_manager.add_target_language_dialog(self.selected_source, self.setSource))
        self.add_category.clicked.connect(lambda: self.category_manager.add_category_modal(self.selected_source, self.selected_target, self.setTarget))
        self.add_translation_button.clicked.connect(lambda: self.translation_manager.add_new_translation_dialog(self.selected_source, self.selected_target, self.selected_category, self.setTarget))
        self.quiz_button.clicked.connect(lambda: self.quiz_manager.generate_quiz(self.selected_source, self.selected_target, self.selected_category))
        self.remove_language_button.clicked.connect(lambda: self.language_manager.remove_source_language_modal(self.selected_source, self.sync_sources))
        self.remove_target_language_button.clicked.connect(lambda: self.language_manager.remove_target_language_modal(self.selected_source,self.selected_target, self.setSource))
        self.remove_category_button.clicked.connect(lambda: self.category_manager.remove_category_modal(self.selected_source, self.selected_target, self.selected_category, self.setTarget))
        self.remove_translation_button.clicked.connect(lambda: self.translation_manager.remove_translation_modal(self.selected_source, self.selected_target, self.selected_category, self.selected_translation, self.setCategory))
        self.reset_filter_by_category.clicked.connect(self.reset_category_filter)
    def setSource(self):
        self.target_language_list.clear()
        self.translations_list.clear()
        self.selected_source = self.source_language_list.currentItem().text()
        self.category_list.clear()
        self.removeCategorySelection()
        langs = self.main_data['translations'][self.selected_source].keys()
        self.target_language_list.addItems(langs)
    def sync_sources(self):
        self.source_language_list.clear()
        self.sources = self.main_data['translations'].keys()
        self.source_language_list.addItems(self.sources)
        
    def setTarget(self):
        self.selected_target = self.target_language_list.currentItem().text()
        self.selected_category = ''
        self.translations_list.clear()
        self.category_list.clear()
        self.syncTranslations(self.main_data['translations'], self.selected_source, self.selected_target, self.selected_category)
        categories = self.main_data['translations'][self.selected_source][self.selected_target].keys()
        self.category_list.addItems(categories)
    
    def setTranslation(self):
        self.selected_translation = self.translations_list.currentItem().text()
        
    def reset_category_filter(self):
        if self.selected_target:
            self.selected_category = ''
            self.setTarget()
        
        
        
    def setCategory(self):
        self.selected_category = self.category_list.currentItem().text()
        self.syncTranslations(self.main_data['translations'], self.selected_source, self.selected_target, self.selected_category)
        
    def removeCategorySelection (self):
        self.category_list.clearSelection()
        
    def syncTranslations(self, loaded_list, source, target, category):
        self.translations_list.clear()
        self.filtered_translations = {}
        if source in loaded_list:
            if target in loaded_list[source]:
                if (category == ''):
                    for category_item in loaded_list[source][target]:
                        categ_list = loaded_list[source][target][category_item]
                        for word in categ_list:
                            self.translations_list.addItem(f"{word} | {categ_list[word]}")
                else: 
                    categ_list = loaded_list[source][target][category]
                    for word in categ_list:
                            self.translations_list.addItem(f"{word} | {categ_list[word]}")
                 

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())  
