from create_user_db import DatingDb
from create_table import TableDb




if __name__ == '__main__':
    db_user_obj = DatingDb('db_dating', 'user_dating')
    db_user_obj.db_user_create()

    TableDb_obj = TableDb('db_dating', 'user_dating')
    TableDb_obj.create_tables()


