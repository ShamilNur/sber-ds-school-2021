import csv

import ego_network_service as service
from config import FRIENDS_FILE, MY_ID


def get_friends(my_id):
    """
    Returns friends of friends from the VKontakte
    and writes to friends_file from the config.
    """

    all_friends = service.load_friends(user_ids=[my_id], deep=False)
    deep_friends = service.load_friends(user_ids=all_friends, deep=True)
    return deep_friends


def get_mutual_friends():
    friend_ids = set()
    with open(FRIENDS_FILE) as file:
        reader = csv.reader(file)
        for row in reader:
            friend_ids.add(int(row[0]))

    service.load_mutual_friends(list(friend_ids))


def friends_from_file():
    """
    Считываем id друзей и друзей друзей из friends.csv
    """
    friend_ids = set()
    with open(FRIENDS_FILE) as file:
        reader = csv.reader(file)
        for row in reader:
            friend_ids.add(int(row[0]))
            friend_ids.add(int(row[1]))

    return friend_ids


def get_friends_info():
    friend_ids = friends_from_file()
    service.load_users_info(list(friend_ids))


def get_friend_groups():
    friend_ids = friends_from_file()
    service.load_groups_info(list(friend_ids))


# 1. Сделать нормальную асинхронность
# 2. Посчитать коэф. Жаккарда по друзьям и группам, смотреть на то, что люди из одного города (3 бинарные переменная)
# И на этих трёх переменных обучить логистическую регрессию, подберём веса и посчитаем отранжированные списки
# Получается, что нужно для каждого человека отобрать список кандидатов в друзья, а потом их отранжировать
# Как это можно сделать: взять список друзей человека, отобрать какое-то количество реально существующих друзей,
# сделать вид, что на самом деле они не друзья, и посмотреть насколько моё ранжирование сможет решить эту задачу.

def main():
    # tempfile module 
    get_friends(MY_ID)
    # get_mutual_friends()
    # get_friends_info()
    # get_friend_groups()


if __name__ == '__main__':
    main()
