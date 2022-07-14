"""
Модуль тестирования методов, функций базы данных.
"""
import unittest
from parameterized import parameterized
from db.create_user_db import DatingDb
from db.create_table import TableDb
from db.insert_data import DataIn
from db.send_data import Parcel
from db.delete_data import Disposal

# Класс тестирования основных функций базы данных.
class FuncTest(unittest.TestCase):
    """
    Данный класс создан для осуществления тестирования ряда значимых функций базы данных при помощи
    библиотеки unittest.
    Атрибуты класса:
    ---------------
    Отсутствуют, не инициализированы.
    Методы класса:
    --------------
    setUpClass
    tearDownClass
    setUp
    tearDown
    test_db_user_create (параметр: db_user_name (str) - название базы данных и название пользователя БД)
    test_create_tables (параметр: table_name (str) - название таблицы БД)
    test_in_elected_table
    test_black_list_output (параметры: user_bot (int) - id пользователя бота, blacklist_user (int) - id пользователя
    из чёрного списка)
    test_del_id_electlist (параметры: user_id (int) - id пользователя бота, del_user_id (int) - id пользователя,
    которого нужно удалить из списка Избранных).
    """

    # Метод запускается перед запуском тестового класса.
    @classmethod
    def setUpClass(cls) -> None:
        """Служебный метод unittest. Запускается перед запуском тестового класса."""
        print(f"Начинается запуск тестового класса {__class__.__name__}")

    # Функция запускается по завершению всех тестов в классе.
    @classmethod
    def tearDownClass(cls) -> None:
        print(f"Закончены все тесты в классе {__class__.__name__}")

    # Функция запускается перед выполнением каждого теста в классе.
    def setUp(self) -> None:
        print("Начат очередной тест в классе!")

    # Функция запускается после каждого теста в классе.
    def tearDown(self) -> None:
        print("Закончен очередной тест в классе!")

    # Тестирование функции db_user_create в методе create_user_db.py.
    @parameterized.expand(
        [
            'db_dating',
            'user_dating'
        ]
    )
    def test_db_user_create(self, db_user_name):
        table_db_obj = DatingDb('db_dating', 'user_dating')
        list_db_user = table_db_obj.db_user_create()
        self.assertIn(db_user_name, list_db_user)

    # Тестирование функции create_tables в методе create_table.py.
    @parameterized.expand(
        [
            'user_data',
            'elected_list',
            'black_list',
            'photo_list',
            'likes_list'
        ]
    )
    def test_create_tables(self, table_name):
        table_db_obj = TableDb('db_dating', 'user_dating')
        list_name_tables = table_db_obj.create_tables()
        self.assertIn(table_name, list_name_tables)

    # Тестирование функции in_elected_table в методе insert_data.py.
    def test_in_elected_table(self):
        insert_data_obj = DataIn('Script_Insert_SQL_table_data.sql', 'db_dating', 'user_dating')
        list_name_tables = insert_data_obj.in_elected_table()
        self.assertEqual(list_name_tables[0], [True, 'Запись 987654320 внесена в список Избранных!'])

    # Тестирование функции black_list_output в методе send_data.py.
    def test_black_list_output(self, user_bot=123456789, blacklist_user=987654321):
        send_data_obj = Parcel('db_dating', 'user_dating')
        list_user = send_data_obj.black_list_output(user_bot)
        self.assertIn(blacklist_user, list_user)

    # Тестирование функции del_id_electlist из метода delete_data.
    def test_del_id_electlist(self, user_id=123456780, del_user_id=987654320):
        del_user_obj = Disposal('db_dating', 'user_dating')
        after_del_list = del_user_obj.del_id_electlist(user_id, del_user_id)
        compare_list = []
        self.assertListEqual(after_del_list, compare_list)


if __name__ == '__main__':
    unittest.main()