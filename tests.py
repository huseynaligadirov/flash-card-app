import unittest
from main import Language, Category, Translations, Quiz, MainWindow
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication


class TestFlashCardApp(unittest.TestCase):

    def setUp(self):
        self.app = QApplication([])
        self.main_window = MainWindow()
        self.translations = {}
        self.data = {
            "categories": ['Test'],
            "languages": ['Aze', 'En'],
            "translations": {
                'Aze': {
                    'En': {
                        'Test': {
                            'test_word': 'translation_word'
                        }
                    }
                }
            },
            "progress": {}
        }

        
    def test_add_new_language(self):
        language_code = "French"
        source = MagicMock()  
        target = MagicMock()  
        dialog = MagicMock()  
        self.main_window.language_manager.add_new_language(language_code, source, target, dialog)
        self.assertIn(language_code, self.main_window.main_data['languages'])
        source.addItem.assert_called_once_with(language_code)
        target.addItem.assert_called_once_with(language_code)
        dialog.accept.assert_called_once()

    def test_add_new_category(self):
        category_name = "Colors"
        categories_list = MagicMock() 
        dialog = MagicMock()  
        self.main_window.category_manager.add_new_category(category_name, categories_list, dialog)
        categories_list.addItem.assert_called_once_with(category_name)
        self.assertIn(category_name, self.main_window.main_data['categories'])
        dialog.accept.assert_called_once()

    def test_quiz_answer_check (self):
        source = 'Aze'
        target = 'En'
        category = 'Test'
        question = 'test_word'
        input = 'translation_word'
        correct = self.main_window.quiz_manager.findAnswer(self.data, source, target, category, question )
        self.assertIn(input, correct)
    def test_add_new_translation(self):
        translation_data = {
            'source': 'source_language',
            'target': 'target_language',
            'category': 'category',
            'word': 'word', 
            'translation': 'translation'
        }

        result = {
            translation_data['source']: {
                translation_data['target']: {
                    translation_data['category']: {
                        translation_data['word']: translation_data['translation']
                    }
                }
            }
        }

        self.data['translations'][translation_data['source']] = result[translation_data['source']]
        self.assertEqual(True, translation_data['source'] in self.data['translations'] )
        
         


    
if __name__ == '__main__':
    unittest.main()
