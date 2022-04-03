# Командный проект по курсу «Профессиональная работа с Python»

## VKinder

### Цель проекта

Цель командного проекта - разработать программу-бота для взаимодействия с базами данных социальной сети. Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

Вам предстоит:
- разработать программу-бота на Python
- спроектировать и реализовать базу данных (БД) для программы
- настроить взаимодействие бота с ВК
- написать документацию по использованию программы

В результате выполнения этого задания вы:
- получите практический опыт работы в команде
- прокачаете навыки коммуникации и умение выполнять задачи в срок
- закрепите навыки работы с GitHub и программирования на языке Python
- разработаете с нуля полноценный программный продукт, который можно будет добавить в портфолио бэкенд-разработчика.

------

### Чеклист готовности к работе над проектом

1. Изучили «Инструкцию по выполнению командного проекта» и «Правила работы в команде» в личном кабинете.
1. Знаете, кто с вами в команде.
1. Познакомились со своей командой и определились, каким способом будете общаться (переписка в любом мессенджере, видеозвонки).
1. Договорились, кто будет размещать общий репозиторий проекта и отправлять его на проверку.
1. У вас должен быть установлен Python 3.x и любая IDE. Мы рекомендуем работать с Pycharm.
1. Настроен компьютер для работы с БД PostgreSQL.
1. Установлен git и создан аккаунт на Github.
1. Должна быть создана группа во Вконтакте, от имени которой будет общаться разрабатываемый бот. Инструкцию можно будет посмотреть [здесь](group_settings.md).

Если все этапы чеклиста пройдены, то можете стартовать работу над проектом. Успехов в работе!

------

### Инструменты/ дополнительные материалы, которые пригодятся для выполнения задания

1. [Python](https://www.python.org/) + IDE([Pycharm](https://www.jetbrains.com/ru-ru/pycharm/download))
2. [Git](https://git-scm.com/) + [Github](https://github.com/)
3. [Postgre](https://www.postgresql.org/) + [PgAdmin](https://www.pgadmin.org/)

------

### Инструкция к работе над проектом

Необходимо разработать программу-бота, которая должна выполнять следующие действия:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с пользователем в ВК, сделать поиск других людей (других пользователей ВК) для знакомств.
2. У тех людей, которые подошли под критерии поиска, получить три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводить в чат с ботом информацию о пользователе в формате:
```
Имя Фамилия
ссылка на профиль
три фотографии в виде attachment(https://dev.vk.com/method/messages.send)
```
4. Должна быть возможность перейти к следующему человеку с помощью команды или кнопки.
5. Сохранить пользователя в список избранных.
6. Вывести список избранных людей.

Поскольку проект рассчитан на командную работу, поэтому каждый пункт делается отдельным человеком. 
Условное разделение на этапы и работу участников.

#### 1 этап:
	1. Участник А. Создание общего репозитория на github. Для предоставления доступа другим участникам необходимо зайти в `Settings` репозитория проекта, найти раздел `Collaborators`, кликнуть по кнопке `Add people`, добавить ник напарника и выбрать роль `Admin`.
	2. Участник Б: Спроектировать БД. В БД должно быть создано минимум 3 таблицы. 
#### 2 этап:
	1. Участник А: Разработать взаимодействие с ВК для получения информации о пользователях и их фотографий. Можно использовать готовые библиотеки.
	2. Участник Б: Реализовать БД для программы с помощью PostgreDB. Приложите скрипты для создания таблиц, чтобы преподаватель смог создать у себя БД. Можно использовать ORM.
#### 2 этап:	
	1. Участник А: Разработать взаимодействие с ботом. Можно воспользоваться этим [шаблоном](basic_code.py) . Будет плюсом, если вы добавите кнопки для более удобного взаимодействия с пользователем.
	2. Участник Б: Интеграция бота и БД.
	5. Участник Б: Написать документацию.

------

### Дополнительные требования к проекту (необязательные для получения зачёта)

1. Получать токен от пользователя с нужными правами.
2. Добавлять человека в чёрный список, чтобы он больше не попадался при поиске, используя БД.
3. Создать кнопки в чате для взаимодействия с ботом.
4. Добавить возможность ставить/убирать лайк выбранной фотографии.
5. К списку фотографий из аватарок добавлять список фотографий, где отмечен пользователь.
6. В ВК максимальная выдача при поиске - 1000 человек. Подумать, как это ограничение можно обойти.
7. Можно усложнить поиск, добавив поиск по интересам. Разбор похожих интересов (группы, книги, музыка, интересы) нужно будет провести с помощью анализа текста.
8. У каждого критерия поиска должны быть свои веса, то есть совпадение по возрасту должно быть важнее общих групп, интересы по музыке - важнее книг, наличие общих друзей - важнее возраста и т.д.

------

### Правила сдачи работы

- разработан бот и все части кода объединены в главной ветке (master/main)
- один из участников команды добавил ссылку на публичный репозиторий в личном кабинете в поле «Ссылка на решение» и в поле «Отправить на проверку эксперту» проставил галочку

------

### Критерии оценки

Зачёт по разработанному проекту может быть получен, если созданный программный продукт соответствует следующим критериям:

1. Отсутствуют ошибки (traceback) во время выполнения программы.
2. Результат программы записывается в БД. Количество таблиц должно быть не меньше трех. Приложена схема БД.
3. Программа добавляет человека в избранный список, используя БД.
4. При повторном поиске в списке люди не повторяются.
5. Программа декомпозирована на функции/классы/модули/пакеты.
6. Написана документация по использованию программы.
7. Код программы удовлетворяет PEP8. Перед отправкой решения на проверку проверьте код с помощью линтеров.

Зачёт ставится всем студентам-участникам команды при выполнении всех требований командного проекта
