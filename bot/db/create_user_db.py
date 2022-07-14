import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import exc


# Класс DatingDb для базы данных к чат-боту Dating на VK
class DatingDb:
    """

    """

    # Функция инициализации класса DatingDb
    def __init__(self, data_base, user):
        """
        :param data_base:
        :param user:
        """
        self.data_base = data_base
        self.user = user

    @staticmethod
    # Функция чтения и возврата пароля из файла sqlpsw.txt
    def sql_psw():
        """
        Функция sql_psw предназначена для чтения и возврата пароля
        из файла sqlpsw.txt
        :return: psw
        """
        with open('sqlpsw.txt', 'r', encoding='utf-8') as file:
            psw = file.read().strip()
        return psw

    # Функция создания базы данных и пользователя
    def db_user_create(self):
        """
        Функция db_user_create создаёт базу данных 'db_dating'
         и пользователя 'user_dating'.
        :return: list_db_user_names
        """
        list_db_user_names = []
        pswd = DatingDb.sql_psw()
        db = f'postgresql://postgres:{pswd}@localhost:5432/{self.data_base}'
        engine = sqlalchemy.create_engine(db)
        if not database_exists(engine.url):
            create_database(engine.url)
        result_db = database_exists(engine.url)
        connection = engine.connect()
        try:
            connection.execute(f"CREATE USER {self.user} WITH PASSWORD '{pswd}';")
            result_user = f'User "{self.user}" exist.'
        except sqlalchemy.exc.ProgrammingError:
            result_user = f'User "{self.user}" already exist.'
        connection.execute(f"ALTER DATABASE {self.data_base} OWNER TO {self.user};")
        list_db_user_names.append(self.data_base)
        list_db_user_names.append((self.user))
        list_db_user_names.append(result_db)
        list_db_user_names.append(result_user)
        return list_db_user_names
