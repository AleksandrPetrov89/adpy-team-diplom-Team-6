import sqlalchemy
from create_user_db import DatingDb

#
class TableDb:
    """

    """

    # Функция инициализации класса TableDb
    def __init__(self, data_base, user):
        """

        :param data_base:
        :param user:
        """
        self.data_base = data_base
        self.user = user

    #
    def db_connect(self):
        """

        :return: connect
        """
        pswd = DatingDb.sql_psw(DatingDb)
        user_db = f'postgresql://{self.user}:{pswd}@localhost:5432/{self.data_base}'
        engine = sqlalchemy.create_engine(user_db)
        connect = engine.connect()
        return connect

    # Функция создания таблиц в базе данных
    def create_tables(self):
        """
        Функция create_tables создаёт нужное кол-во таблиц и в конце работы выводит их список.
        :return: tables_list
        """
        TableDb_obj = TableDb(self.data_base, self.user)
        connect = TableDb_obj.db_connect()
        tables_list = []
        sql_table = 'CREATE TABLE IF NOT EXISTS'
        dict_tables = {
            'user_data': ['user_id INTEGER PRIMARY KEY,', 'profile_link VARCHAR(60),',
                          'age INTEGER CHECK(age<150),', 'first_name VARCHAR(40),', 'last_name VARCHAR(40),',
                          'sex INTEGER,', 'city VARCHAR(60),', 'token VARCHAR(120),', 'groups INTEGER,',
                          'interests TEXT,', 'music TEXT,', 'books TEXT,',
                          'photo_link_1 VARCHAR(120),', 'photo_link_2 VARCHAR(120),',
                          'photo_link_3 VARCHAR(120)'],
            'elected_list': ['user_data_user_id INTEGER NOT NULL REFERENCES user_data(user_id),',
                             'bot_user_user_id INTEGER NOT NULL REFERENCES user_data(user_id)'],
            'black_list': ['user_data_user_id INTEGER NOT NULL REFERENCES user_data(user_id),',
                           'bot_user_user_id INTEGER NOT NULL REFERENCES user_data(user_id)']
        }
        for tbl_name, tbl_col in dict_tables.items():
            if tbl_name == 'user_data':
                req = f"{sql_table} {tbl_name} ("
                for item in range(len(tbl_col)):
                    req += f"{tbl_col[item]} "
                req = req + ");"
            elif tbl_name == 'black_list' or tbl_name == 'elected_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]});"
            connect.execute(req)
            tables_list.append(tbl_name)
        return tables_list
