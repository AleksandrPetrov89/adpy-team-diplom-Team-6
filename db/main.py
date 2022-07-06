from create_user_db import Dating_Db
from create_table import Table_Db




if __name__ == '__main__':
    db_user_obj = Dating_Db('db_dating', 'user_dating')
    db_user_obj.db_user_create()
    table_db_obj = Table_Db('db_dating', 'user_dating')
    table_db_obj.create_tables()
