from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QListWidget
from save import DataManager
class Category:
    categories = set()
    
    def __init__(self, main_data):
        self.data = main_data
        self.data_manager = DataManager()

    def add_category(self, category_name):
        self.categories.add(category_name)

    def remove_category(self, category_name):
        self.categories.remove(category_name)

    def list_categories(self):
        return list(self.categories)

    def add_new_category_dialog(self, categories_list):
        dialog = QDialog()
        dialog.setWindowTitle("Add Category")
        layout = QVBoxLayout(dialog)
        category_label = QLabel("Category Name:", dialog)
        category_input = QLineEdit(dialog)
        layout.addWidget(category_label)
        layout.addWidget(category_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        buttons.accepted.connect(lambda: self.add_new_category(category_input.text(), categories_list, dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec_()

    def add_new_category(self, category_name, categories_list, dialog):
        categories_list.addItem(category_name)
        categories = self.data['categories']
        categories.append(category_name)
        self.data['categories'] = categories
        self.data_manager.saveData(self.data)
        dialog.accept()
