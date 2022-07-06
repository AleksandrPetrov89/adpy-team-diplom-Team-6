import sqlalchemy
from create_user_db import Dating_Db

#
class Table_Db:
    """

    """

    # Функция инициализации класса Table_Db
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
        pswd = Dating_Db.sql_psw(Dating_Db)
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
        table_db_obj = Table_Db(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        tables_list = []
        sql_table = 'CREATE TABLE IF NOT EXISTS'
        dict_tables = {
            'user_data': ['id SERIAL PRIMARY KEY,', 'user_id INTEGER NOT NULL,', 'profile_link VARCHAR(60) NOT NULL,',
                          'age INTEGER CHECK(age<150),', 'first_name VARCHAR(40),', 'last_name VARCHAR(40),',
                          'sex INTEGER,', 'city VARCHAR(60),', 'token VARCHAR(80),', 'groups INTEGER,',
                          'interests VARCHAR(100),', 'music VARCHAR(100),', 'books VARCHAR(100),',
                          'photo_link_1 VARCHAR(60) NOT NULL,', 'photo_link_2 VARCHAR(60) NOT NULL,',
                          'photo_link_3 VARCHAR(60) NOT NULL'],
            'elected_list': ['id SERIAL PRIMARY KEY,', 'date_creating DATE,',
                             'user_data_id INTEGER NOT NULL REFERENCES user_data(id)'],
            'black_list': ['id SERIAL PRIMARY KEY,', 'user_data_id INTEGER NOT NULL REFERENCES user_data(id)'],
            'bot_user': ['id SERIAL PRIMARY KEY,', 'user_data_id INTEGER NOT NULL REFERENCES user_data(id),',
                         'elected_list_id INTEGER NOT NULL REFERENCES elected_list(id)']
        }
        for tbl_name, tbl_col in dict_tables.items():
            if tbl_name == 'user_data':
                req = f"{sql_table} {tbl_name} ("
                for item in range(len(tbl_col)):
                    req += f"{tbl_col[item]} "
                req = req + ");"
            elif tbl_name == 'black_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]});"
            elif tbl_name == 'bot_user' or 'elected_list':
                req = f"{sql_table} {tbl_name} ({tbl_col[0]} {tbl_col[1]} {tbl_col[2]});"
            connect.execute(req)
            tables_list.append(tbl_name)
        return tables_list
