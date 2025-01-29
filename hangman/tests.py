import unittest
from unittest.mock import patch
import random

# Импортируем функции, которые будем тестировать
from hangman.game import select_word, load_words  # Замените your_module на имя вашего модуля

class TestSelectWord(unittest.TestCase):
    def setUp(self):
        # Подготовим тестовый список слов
        self.words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

    @patch('builtins.input', side_effect=["5"])  # Подменяем ввод пользователя
    def test_select_word_valid_input(self, mock_input):
        """
        Тестируем корректный ввод: пользователь вводит допустимое количество букв.
        """
        result = select_word(self.words)
        self.assertIn(result, ["apple", "grape"])  # Слова длиной 5

    @patch('builtins.input', side_effect=["1", "5"])  # Первый ввод некорректен, второй корректен
    def test_select_word_invalid_then_valid_input(self, mock_input):
        """
        Тестируем случай, когда пользователь сначала вводит некорректное значение,
        а затем корректное.
        """
        result = select_word(self.words)
        self.assertIn(result, ["apple", "grape"])  # Слова длиной 5

    @patch('builtins.input', side_effect=["abc", "5"])  # Первый ввод некорректен (не число), второй корректен
    def test_select_word_non_numeric_input(self, mock_input):
        """
        Тестируем случай, когда пользователь вводит нечисловое значение,
        а затем корректное.
        """
        result = select_word(self.words)
        self.assertIn(result, ["apple", "grape"])  # Слова длиной 5



if __name__ == "__main__":
    unittest.main()