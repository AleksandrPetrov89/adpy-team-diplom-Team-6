from create_user_db import DatingDb
from create_table import TableDb
from insert_data import DataIn


# Класс взаимодействия
class Interaction:
    """

    """
    # Функция инициализации класса
    def __init__(self):
        pass


    # Получение запроса на внесение данных пользователей в таблицу user_data
    def getreq_in_userdata(self, status=True):
        """
        :return: status
        """
        if status:
            write_file_obj = DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table,
                                 self.data_base, self.user)
            write_file_obj.write_file()
            ins_userdata_obj = DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table,
                                 self.data_base, self.user)
            ins_userdata_obj.insert_user_table()
        else:
            status = False
        return status

    # Получение запроса на внесение данных пользователя в таблицу Избранных (elected_list)
    def getreq_in_elected(self, status=True):
        """
        :return: status
        """
        if status:
            elect_user_obj = DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table,
                                 self.data_base, self.user)
            elect_user_obj.in_elected_table()
        else:
            status = False
        return status

    # Получение запроса на внесение данных пользователя в таблицу Чёрный список (black_list)
    def getreq_in_blacklist(self, status=True):
        """
        :return: status
        """
        if status:
            blacklist_obj = DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table,
                                    self.data_base, self.user)
            blacklist_obj.in_blacklist_table()
        else:
            status = False
        return status




if __name__ == '__main__':
    # Создание базы данных и пользователя
    db_user_obj = DatingDb('db_dating', 'user_dating')
    db_user_obj.db_user_create()

    # Создание всех таблиц в соответствии с заданием
    TableDb_obj = TableDb('db_dating', 'user_dating')
    TableDb_obj.create_tables()


