from db.create_table import TableDb


#
class PhotoTransfer:
    """

    """
    # Функция инициализации класса PhotoTransfer
    def __init__(self, data_base, user):
        self.data_base = data_base
        self. user = user

    # Функция вывода из базы данных списка фотографий для пользователя user_id,
    # на которых он поставил "лайк" с проверкой на дублирование.
    def likes_photo_output(self, user_id=123456789):
        """
        Функция likes_photo_output принимает на вход id пользователя и выводит список списков фотографий
        для пользователя user_id, на которых он поставил "лайк". Во внутренние списки помещена информация:
        ссылка на фото (тип str), ID фотографии (тип int), ID пользователя, который поставил "лайк"
        на фото(тип данных int). В случае, если в БД нет пользователя с переданным на вход id,
        то возвращается пустой список. Выведенный список исключает повторение записей в нём.
        :return: result_lp_output_list
        """
        photo_list = []
        result_lp_output_list = []
        table_db_obj = TableDb(self.data_base, self.user)
        connect = table_db_obj.db_connect()
        req_output = f'SELECT pl.photo_link, pl.photo_id, ll.user_data_user_id FROM photo_list pl ' \
                     f'JOIN likes_list ll ON ll.photo_list_id = pl.id JOIN user_data ud ON ' \
                     f'll.user_data_user_id = ud.user_id WHERE ll.user_data_user_id = {user_id};'
        output_list = connect.execute(req_output).fetchall()
        for item_list in output_list:
            clean_id = ''
            for symbol in str(item_list):
                if symbol != "'" and symbol != "(" and symbol != ")":
                    clean_id += symbol
            photo_list.append(clean_id)
        photo_list = list(set(photo_list))
        for item in photo_list:
            result_lp_output_list.append(item.split(", "))
        for new_item in result_lp_output_list:
            if new_item[1].isdigit():
                new_item[1] = int(new_item[1])
            if new_item[2].isdigit():
                new_item[2] = int(new_item[2])
        return result_lp_output_list


if __name__ == '__main__':
    PhotoTransfer.likes_photo_output(PhotoTransfer('db_dating', 'user_dating'))
