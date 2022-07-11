from db.create_table import TableDb


#
class DelPhoto:
    """

    """
    # Функция инициализации класса DelPhoto.
    def __init__(self, data_base, user):
        self.data_base = data_base
        self. user = user

    # Функция удаления лайкнутых фото из двух списков: photo_list, likes_list.
    def del_id_photolist(self, bot_user_id=123456789, user_id=987654321, del_photo_id=111111111):
        """
        Функция del_id_photolist принимает на вход три параметра: id пользователя бота, id пользователя,
        фотографию которого нужно удалить и id самой фотографии.
        Удаляет данные о фото в списках photo_list, likes_list. В результате выполнения возвращает
        пустой список after_del_list.
        :return: after_del_list
        """
        clean_id_list = []
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        req_search_id = f'SELECT id FROM photo_list WHERE photo_id={del_photo_id} AND user_data_user_id={user_id};'
        list_photo_list_id = connect.execute(req_search_id).fetchall()
        for item_list in list_photo_list_id:
            for id_value in item_list:
                clean_id_list.append(id_value)
        for ids in clean_id_list:
            req_del_id_ll = f'DELETE FROM likes_list WHERE bot_user_user_id={bot_user_id} AND ' \
                            f'photo_list_id={ids};'
            connect.execute(req_del_id_ll)
        req_del_id_pl = f'DELETE FROM photo_list WHERE user_data_user_id={user_id} AND photo_id={del_photo_id};'
        connect.execute(req_del_id_pl)
        req_search_id = f'SELECT id FROM photo_list WHERE photo_id={del_photo_id} AND user_data_user_id={user_id};'
        after_del_list = connect.execute(req_search_id).fetchall()
        return after_del_list


# if __name__ == '__main__':
#     DelPhoto.del_id_photolist(DelPhoto('db_dating', 'user_dating'))
