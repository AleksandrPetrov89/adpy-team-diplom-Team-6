import sqlalchemy.exc
from create_table import TableDb


#
class DataIn:
    """

    """

    # Функция инициализации класса Data_In
    def __init__(self, filename, data_base, user):
        self.filename = filename
        self.data_base = data_base
        self.user = user

    # Функция получения данных в виде словаря.
    def get_data(self, user_id=555111666, profile_link='https://vk.com/id123456789', age=16, first_name='Ivan',
                 last_name='Ivanov', sex=2, city='Moscow',
                 token='58eb4fa4a72b028c214dd5c8786d23a7054577f0b5a2530d5459936a9b8f8f58d1edc970fd82581e3e904',
                 groups=555666777, interests='спорт, рыбалка, кино, шахматы', music='рок, техно, джаз, "Битлз", '
                                                                                    '"Дорз"',
                 books='"ghghgh", "ghghgfk tutri", "cbdjdj sletykym"'):
        """

        """
        dict_user = {
            user_id: [profile_link, age, first_name, last_name, sex, city, token, groups, interests,
                      music, books]
        }
        return dict_user

    # Функция зыписывает данные, полученные из функции get_data в файл Script_Insert_SQL_table_data.sql.
    def write_file(self):
        """
        :return: write_result
        """
        write_obj = DataIn(self.filename, self.data_base, self.user)
        with open(self.filename, 'w', encoding='utf-8') as file:
            for keys, item in write_obj.get_data().items():
                insert_text = 'INSERT INTO user_data(user_id, profile_link, age, first_name, last_name, sex, city,' \
                              ' token, groups, interests, music, books)'
                values_text = f' VALUES({keys}'
                file.write(f'{insert_text}')
                for elem in item:
                    if type(elem) != str:
                        values_text += f', {str(elem)}'
                    elif type(elem) == str:
                        values_text += f""", '{elem}'"""
                values_text = values_text + ');'
                file.write(f'{values_text}\n')
        write_result = f'Файл {self.filename} записан.'
        return write_result

    # Функция считывания данных, полученных из файла Script_Insert_SQL_table_data.sql
    def read_file(self):
        """
        :return: read_list
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            read_data = file.readlines()
            read_list = list(item.strip() for item in read_data)
        return read_list

    # Функция заносит данные из файла Script_Insert_SQL_table_data.sql в базу данных в таблицу user_data.
    # Вносятся только новые данные, если какой-то пользователь в таблице есть, то не дублируется.
    def insert_user_table(self):
        """
        Функция insert_user_table даёт возможность записывать данные о пользователях VK в базу данных.
        Последовательность выполняемых операций: данные принимаются в функцию get_data в виде словаря, записываются
        в файл Script_Insert_SQL_table_data.sql в виде SQL-запроса при помощи функции write_file, далее SQL-запрос
        считывается функцией read_file и исполняется. Предусмотрено получение на вход данных в словаре с любым
        количеством ключей. Если словарь пустой, то ничего в базу не записывается. Функция способна записывать в файл
        и исполнять любое количество SQL-запросов.
        :return: insert_result, comment_result
        """
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()

        insert_user_obj = DataIn(self.filename, self.data_base, self.user)
        insert_user_obj.write_file()
        insert_list_data = insert_user_obj.read_file()
        insert_result = True
        comment_result = 'Запись успешно осуществлена!'
        for item in insert_list_data:
            try:
                connect.execute(item.strip())
            except sqlalchemy.exc.IntegrityError:
                comment_result = f'Запись: {item} в таблицу не сделана, т.к. пользователь уже существует!'
                insert_result = False
        return insert_result, comment_result

    # Функция заносит данные переданного пользователя в таблицу Избранных (elected_list),
    # пользователь вносится в поле user_data_user_id с проверкой дублирования.
    def in_elected_table(self, user_bot=123456789, elected_user=987654321):
        """
        Функция занесения пользователя в Избранные (таблица elected_list).
        ID выбранного пользователя помещается в поле user_data_user_id.
        Также осуществляется проверка на дублирование. В случае повторного внесения
        возвращается соответствующая информация.
        :return: insert_result, comment_result
        """
        dict_blacklist_user = {user_bot: elected_user}
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        insert_result = True
        comment_result = f'Запись {elected_user} внесена в список Избранных!'
        for key, value in dict_blacklist_user.items():
            req_sql = f'INSERT INTO elected_list(user_data_user_id, bot_user_user_id) VALUES({value}, {key});'
            user_elect_exist = f'SELECT user_data_user_id, bot_user_user_id FROM elected_list' \
                               f' WHERE user_data_user_id={elected_user} AND bot_user_user_id={user_bot};'
            is_exist = connect.execute(user_elect_exist).fetchall()
            if is_exist != []:
                comment_result = f'Запись: {req_sql} в таблицу не сделана, т.к. пользователь {value} для пользователя' \
                                 f' {key} в Избранных уже существует!'
                insert_result = False
            else:
                connect.execute(req_sql)
        return insert_result, comment_result

    # Функция заносит данные переданного пользователя в Чёрный список (black_list).
    # Заблокированный пользователь вносится в поле user_data_user_id с проверкой дублирования.
    def in_blacklist_table(self, user_bot=123456789, blacklist_user=987654321):
        """
        Функция занесения пользователя в Чёрный список (таблица black_list).
        ID заблокированного пользователя помещается в поле user_data_user_id.
        Также осуществляется проверка на дублирование. В случае повторного внесения
        возвращается соответствующая информация.
        :return: insert_result, comment_result
        """
        dict_blacklist_user = {user_bot: blacklist_user}
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        insert_result = True
        comment_result = f'Запись {blacklist_user} внесена в черный список!'
        for key, value in dict_blacklist_user.items():
            req_sql = f'INSERT INTO black_list(user_data_user_id, bot_user_user_id) VALUES({value}, {key});'
            user_blacklist_exist = f'SELECT user_data_user_id, bot_user_user_id FROM black_list' \
                                   f' WHERE user_data_user_id={blacklist_user} AND bot_user_user_id={user_bot};'
            is_exist = connect.execute(user_blacklist_exist).fetchall()
            if is_exist != []:
                comment_result = f'Запись: {req_sql} в таблицу не сделана, т.к. пользователь {value} для пользователя' \
                                 f' {key} уже существует в Чёрном списке!'
                insert_result = False
            else:
                connect.execute(req_sql)
        return insert_result, comment_result


if __name__ == '__main__':
    DataIn.insert_user_table(DataIn('Script_Insert_SQL_table_data.sql', 'db_dating', 'user_dating'))
    # DataIn.in_blacklist_table(DataIn('Script_Insert_SQL_table_data.sql', 'db_dating', 'user_dating'))
    # DataIn.in_elected_table(DataIn('Script_Insert_SQL_table_data.sql', 'db_dating', 'user_dating'))
