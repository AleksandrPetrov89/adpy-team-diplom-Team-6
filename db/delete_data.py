from create_table import TableDb

#
class Disposal:
    """

    """
    # Функция инициализации класса Disposal
    def __init__(self, data_base, user):
        self.data_base = data_base
        self. user = user

    # Функция удаления из чёрного списка базы данных ID пользователя (del_user_id) для пользователя user_id.
    def del_id_blacklist(self, user_id=123456789, del_user_id=987654321):
        """
        Функция del_id_blacklist принимает на вход id двоих пользователей и удаляет id нужного пользователя,
        который ранее был внесён в чёрный список. В случае, если в БД нет пользователя, для которого выполняется
        удаление, то возвращается пустой список. Если в БД нет пользователя, которого нужно удалить, то возвращается
        черный список. В нём, в качестве подтверждения, не будет пользователя на удаление которого поступил запрос.
        Если чёрный список пуст, то он и будет возвращён.
        :return: after_del_list
        """
        after_del_list = []
        TableDb_obj = TableDb(self.data_base, self.user)
        connect = TableDb_obj.db_connect()
        req_del_id_bl = f'DELETE FROM black_list WHERE bot_user_user_id={user_id} AND user_data_user_id={del_user_id};'
        connect.execute(req_del_id_bl)
        req_del_check = f'SELECT user_data_user_id FROM black_list WHERE bot_user_user_id={user_id};'
        check_list = connect.execute(req_del_check).fetchall()
        for item_list in check_list:
            clean_id = ''
            for symbol in str(item_list):
                if symbol.isdigit():
                    clean_id += symbol
            after_del_list.append(int(clean_id))
        after_del_list = list(set(after_del_list))
        print(after_del_list)
        return after_del_list

    # Функция удаления из списка Избранных базы данных ID пользователя (del_user_id) для пользователя user_id.
    def del_id_electlist(self, user_id, del_user_id):
        """
        Функция del_id_electlist принимает на вход id двоих пользователей и удаляет id нужного пользователя,
        который ранее был внесён в список Избранных. В случае, если в БД нет пользователя, для которого выполняется
        удаление, то возвращается пустой список. Если в БД нет пользователя, которого нужно удалить, то возвращается
        список Избранных. В нём, в качестве подтверждения, не будет пользователя на удаление которого поступил запрос.
        Если список Избранных пуст, то он и будет возвращён.
        :return: after_del_list
        """
        after_del_list = []
        TableDb_obj = TableDb(self.data_base, self.user)
        connect = TableDb_obj.db_connect()
        req_del_id_el = f'DELETE FROM elected_list WHERE bot_user_user_id={user_id} AND ' \
                        f'user_data_user_id={del_user_id};'
        connect.execute(req_del_id_el)
        req_del_check = f'SELECT user_data_user_id FROM elected_list WHERE bot_user_user_id={user_id};'
        check_list = connect.execute(req_del_check).fetchall()
        for item_list in check_list:
            clean_id = ''
            for symbol in str(item_list):
                if symbol.isdigit():
                    clean_id += symbol
            after_del_list.append(int(clean_id))
        after_del_list = list(set(after_del_list))
        print(after_del_list)
        return after_del_list
    

if __name__ == '__main__':
    # Disposal.del_id_blacklist(Disposal('db_dating', 'user_dating'))
    Disposal.del_id_electlist(Disposal('db_dating', 'user_dating'))
