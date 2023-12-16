import unittest
from pygame import Pawn 
from pygame import Rook

class TestPawnFunction(unittest.TestCase):

    def test_black_pawn_moves(self):
        position = (3, 1)
        color = 'black'
        black_locations = [(2, 2), (4, 2)]
        white_locations = [(3, 2)]
        result = Pawn(position, color, black_locations, white_locations)
        self.assertEqual(result, [(3, 2), (2, 2), (4, 2)])

    def test_white_pawn_moves(self):
        position = (3, 6)
        color = 'white'
        black_locations = [(3, 5), (4, 5)]
        white_locations = [(2, 5)]
        result = Pawn(position, color, black_locations, white_locations)
        self.assertEqual(result, [(3, 5), (2, 5), (4, 5)])

    def test_no_enemy_to_attack(self):
        position = (5, 1)
        color = 'black'
        black_locations = [(6, 2)]
        white_locations = [(5, 2)]
        result = Pawn(position, color, black_locations, white_locations)
        self.assertEqual(result, [(6, 2)])

    def test_blocked_pawn(self):
        position = (3, 1)
        color = 'black'
        black_locations = [(2, 2), (4, 2), (3, 2)]
        white_locations = []
        result = Pawn(position, color, black_locations, white_locations)
        self.assertEqual(result, [])

class TestRook(unittest.TestCase):
    """
    Класс для тестирования функции Rook.

    :setUp: Метод, выполняемый перед каждым тестом, задает начальные значения.
    :test_rook_moves_white: Тест для ладьи белого цвета.
        :returns: Сравнивает результат выполнения Rook с ожидаемым результатом.
        :rtype: None
    :test_rook_moves_black: Тест для ладьи черного цвета.
        :returns: Сравнивает результат выполнения Rook с ожидаемым результатом.
        :rtype: None
    :test_rook_blocked_path: Тест для ладьи с заблокированным путем.
        :returns: Сравнивает результат выполнения Rook с ожидаемым результатом.
        :rtype: None
    """
    def setUp(self):
        """
        Задает начальные значения для тестов.
        :returns: None
        :rtype: None
        """
        self.black_locations = [(1, 1), (2, 2), (3, 3)]  # Пример для черных фигур
        self.white_locations = [(5, 5), (6, 6), (7, 7)]  # Пример для белых фигур

    def test_rook_moves_white(self):
        # Тест для ладьи белого цвета
        result = Rook((4, 4), 'white')
        expected = [(5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7)]
        self.assertEqual(result, expected)

    def test_rook_moves_black(self):
        """
        Тест для ладьи белого цвета.

        :returns: Сравнивает результат выполнения Rook с ожидаемым результатом.
        :rtype: None
        """
        result = Rook((4, 4), 'black')
        expected = [(1, 4), (2, 4), (3, 4), (4, 1), (4, 2), (4, 3)]
        self.assertEqual(result, expected)

    def test_rook_blocked_path(self):
        """
        Тест для ладьи черного цвета.

        :returns: Сравнивает результат выполнения Rook с ожидаемым результатом.
        :rtype: None
        """
        self.black_locations.append((5, 4))  # Заблокируем путь ладьи
        result = Rook((4, 4), 'white')
        expected = [(6, 4), (7, 4), (4, 5), (4, 6), (4, 7)]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()