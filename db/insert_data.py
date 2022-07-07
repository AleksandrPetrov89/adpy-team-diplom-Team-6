import sqlalchemy
from create_table import TableDb

#
class DataIn:
    """

    """
    # Функция инициализации класса Data_In
    def __init__(self, filename, user_table, elected_table, black_list_table, data_base, user):
        self.filename = filename
        self.user_table= user_table
        self.elected_table = elected_table
        self.black_list_table = black_list_table
        self.data_base = data_base
        self.user = user


    # Функция получения данных в виде словаря
    def get_data(self):
        """

        """
        dict_user = {
                    123456789 : ['https://vk.com/id123456789', 16, 'Ivan', 'Ivanov', 'Moscow',
                    'fdjfhdjfhdjfdjd85588gjgfjkgfkk5885485486965u569gjjg',
                    555555555, '', '', '','https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos715243021',
                    'https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos715243021',
                    'https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos715243021'],
                    987654321 : ['https://vk.com/id563456789', 45, 'Ighkjfgjgf', 'fjhgdfkj', 'Kirov',
                    'fdjfhdjfhdjfdjd85588gjgfjkgfkk58rhtrhtrhtrht54455456456grgjg',
                    195967986, 'bgbkhkg', 'bdfbdbggbd', 'bdfgbdbgdggbdbgfgbdfbf',
                    'https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos715243021',
                    'https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos715243021',
                    'https://vk.com/id715243021?z=photo715243021_457239017%2Fphotos715243021']
        }
        return dict_user

    # Функция зыписывает данные, полученные из функции get_data в файл
    def write_file(self):
        """
        :return: write_result
        """
        write_obj = DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table, self.data_base,
                           self.user)
        insert_text = 'INSERT INTO user_data(user_id, profile_link, age, first_name, last_name, city,' \
                      ' token, groups, interests, music, books, photo_link_1, photo_link_2, photo_link_3)'
        with open(self.filename, 'w', encoding='utf-8') as file:
            for keys, item in write_obj.get_data().items():
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

    # Функция поиска и замены спецсимвола % в ссылках и замена на %%, в противном случае
    # данные не записываются в таблицы
    def search_link_simbol(self):
        """
        :return: new_list_for_req
        """
        search_obj = DataIn.read_file(DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table,
                                 self.data_base, self.user))
        new_list_for_req = []
        for item in search_obj:
            text_list = item.split(',')
            indexes = [14, 24, 25, 26]
            for index in indexes:
                if '%' in text_list[index]:
                    new_text_link = text_list[index].replace('%', '%%')
                    text_list[index] = new_text_link
            new_str_for_req = ','.join(text_list)
            new_list_for_req.append(new_str_for_req)
        return new_list_for_req

    # Функция заносит данные из файла Script_Insert_SQL_table_data.sql в таблицу user_data
    def insert_user_table(self):
        """
        :return: insert_result, comment_result
        """
        TableDb_obj = TableDb(self.data_base, self.user)
        connect = TableDb_obj.db_connect()

        insert_user_obj = DataIn(self.filename, self.user_table, self.elected_table, self.black_list_table,
                                 self.data_base, self.user)
        insert_list_data = insert_user_obj.search_link_simbol()
        insert_result = True
        comment_result = 'Все записи сделаны!'
        for item in insert_list_data:
            try:
                connect.execute(item.strip())
            except sqlalchemy.exc.IntegrityError:
                comment_result = f'Запись: {item} в таблицу не сделана, т.к. пользователь уже существует!'
                insert_result = False
        return insert_result, comment_result



if __name__ == '__main__':
    DataIn.insert_user_table(DataIn('Script_Insert_SQL_table_data.sql', 'user_data', 'elected_list', 'black_list',
                                    'db_dating', 'user_dating'))