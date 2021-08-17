import asyncio
import csv
from typing import List

import vk_api
from tqdm import tqdm

from config import *

session = vk_api.VkApi(token=TOKEN)
vk = session.get_api()


def load_friends(user_ids: List[int], deep: bool = False):
    """
    Логика получения отдельного пользователя выделена в отдельную асинхронную функцию.
    read https://vk.com/dev/friends.get
    """

    if deep:
        async def get_deep_friends(user_id):
            print(f"Task with user_id {user_id}...")
            friend_params = {
                'user_id': str(user_id)
            }
            friends_resp = session.method(method='friends.get', values=friend_params)

            with open(FRIENDS_FILE, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                for friend_id in friends_resp['items']:
                    writer.writerow((user_id, friend_id))

            await asyncio.sleep(1)

        # Изначально сформируем корутины (сопрограммы)
        async def create_load_friend_coroutines():
            requests = [get_deep_friends(user_id) for user_id in user_ids]
            await asyncio.gather(*requests)

        asyncio.run(create_load_friend_coroutines())
    else:
        print(f"Task with user_id {user_ids[0]}...")
        friend_params = {
            'user_id': str(user_ids[0])  # contains only my_id
        }
        friends_resp = session.method(method='friends.get', values=friend_params)
        return friends_resp['items']


def load_mutual_friends(friend_ids: List):
    """
    read https://vk.com/dev/friends.getMutual
    """

    result = dict()

    # Количество id пользователей, с которыми необходимо искать общих друзей должно составлять не более 100.
    step = 100
    for part in range(0, len(friend_ids), step):
        part_ids = friend_ids[part: part + step]
        print('part:', part, 'part + step - 1:', part + step)

        # Нужно передать список id пользователей, разделённых запятыми.
        mutual_params = {
            'source_uid': MY_ID,
            'target_uids': ','.join(str(i) for i in part_ids)
        }
        try:
            mutual_resp = session.method(method='friends.getMutual', values=mutual_params)
        except vk_api.exceptions.ApiError:
            # [18] User was deleted or banned
            # [30] This profile is private
            continue

        for m in mutual_resp:
            result[m['id']] = m.get('common_friends', None)

    # Запишем всю информацию в файл
    with open(MUTUAL_FRIENDS_FILE, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['FriendId', 'CommonFriendId'])
        for friend_id, common_ids in result.items():
            for common_id in common_ids:
                writer.writerow((friend_id, common_id))

    return result


def load_users_info(user_ids: List):
    """
    read https://vk.com/dev/users.get
    """

    result = dict()
    print('len', len(user_ids))

    # Чтобы не сталкиваться с ошибкой 413 Request Entity Too Large, нужно укладываться в 2048 символов.
    # Кроме того, для API ВКонтакте количество переданных user_id должно составлять не более 1000.
    step = 1000
    for part in range(0, len(user_ids), step):
        part_ids = user_ids[part: part + step]
        print('part:', part, 'part + step - 1:', part + step)

        # Нужно передать список id, разделённых через запятую
        user_params = {
            'user_ids': ','.join(str(i) for i in part_ids),
            'fields': 'sex, bdate, city'
        }
        users_resp = session.method(method='users.get', values=user_params)

        for u in users_resp:
            result[u['id']] = {
                'first_name': u.get('first_name', None),
                'last_name': u.get('last_name', None),
                'sex': u.get('sex', None),
                'bdate': u.get('bdate', None),
                'city': u.get('city', {}).get('title', None)
            }

    # TODO: записывать сразу при получении
    # Запишем всю информацию в файл
    with open(FRIENDS_DESC_FILE, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['FirstName', 'LastName', 'Sex', 'Bdate', 'City'])
        for user_id, desc in result.items():
            writer.writerow((user_id, *list(desc.values())))

    return result


def load_groups_info(user_ids: List):
    """
    read https://vk.com/dev/groups.get
    """

    result = dict()
    groups_info = dict()

    # TODO: сформировать корутины в цикле: async def func() asyncio.gather (и вызвать await):
    for user_id in tqdm(user_ids, position=0, leave=False, colour='green', ncols=80):

        # Нужно передать user_id.
        # Параметр fields учитывается только при extended=1.
        user_params = {
            'user_id': str(user_id),
            'extended': bool(1),
            'filter': 'publics',
            'fields': 'description',
            'count': '75'
        }
        try:
            users_resp = session.method(method='groups.get', values=user_params)
        except vk_api.exceptions.ApiError:
            # TODO: можно сделать deque
            # [30] This profile is private
            continue

        result[user_id] = list()
        for group in users_resp['items']:
            result[user_id].append({
                'group_id': group.get('id', None)
            })

            if group.get('id') not in groups_info:
                groups_info[group.get('id')] = {
                    'name': group.get('name', None),
                    'screen_name': group.get('screen_name', None),
                    'type': group.get('type', None),
                    'description': group.get('description', None)
                }

    # Запишем полученную информацию в 2 файла:
    # 1) в friend_groups.csv - список сообществ, в которых состоит пользователь;
    # 2) в groups_desc.csv - описание каждого сообщества.
    with open(FRIEND_GROUPS_FILE, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['UserId', 'GroupId'])
        for user_id, groups in result.items():
            for group in groups:
                writer.writerow((user_id, group['group_id']))

    with open(GROUPS_DESC_FILE, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['GroupId', 'Name', 'ScreenName', 'Type', 'Description'])
        for group_id, group_desc in groups_info.items():
            writer.writerow((group_id, *list(group_desc.values())))

    return result
