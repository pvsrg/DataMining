def popnitems(dic, nmb):
    for i in range(nmb):
        try:
            key, val = dic.popitem()
            yield key, val
        except KeyError:
            yield None, None


class FriendPath:

    def __init__(self, name):
        self.name = name
        self.path = {}
        self.step = {}
        self.next_step = {}
        self.users_for_run = {}
        self.users_running = {}
        self.share_friend = None
        self.stop = False
        self.towards_path = None

    def set_towards_path(self, towards_path):
        self.towards_path = towards_path

    def check_share_friend(self, user_id):
        if self.path.get(user_id, None) is None:
            return False
        else:
            self.share_friend = user_id
            self.stop = True
            return True

    def start(self, user_start):
        self.users_for_run = {}
        self.users_for_run.update(user_start)

    def get_user(self):
        for user, values in self.users_for_run.items():
            self.users_running[user] = values
            yield user
        self.users_for_run = {}

    def put_friends(self, user_id, friends):

        # Проверяем остановлена обработка или нет
        if self.stop:
            return

        # Проверяем взаимоподписаны два автора или нет
        friend = self.users_running[user_id][1]
        if (friends.get(friend) is not None) or (friend is None):
            # Взаимоподписаны, добавляем в путь, а друзей друга добавляем в следующий шаг
            self.path[user_id] = self.users_running.pop(user_id, [None, None])
            self.next_step.update(
                {id: [name, user_id] for id, name in friends.items() if self.path.get(id, 'not') == 'not'})
            # Проверяем найден ли общий друг, если найден - то прекращаем поиск
            if self.towards_path.check_share_friend(user_id):
                self.share_friend = user_id
                self.stop = True
                for friend in self.make_full_path():
                    print(friend)
                return
        else:
            # Не взаимоподписаны, поэтому не добавляем в путь
            self.users_running.pop(user_id, None)

        # Проверяем исчерпан ли текущий шаг
        if len(self.users_running) == 0:
            # Шаг исчерпан, переходим на следующий шаг
            self.step, self.next_step = self.next_step, {}
            if not len(self.step):
                # Авторы образовали замкнутую группу, достич целевого автора не получится
                self.stop = True
                return
            number_for_run = 3
        else:
            number_for_run = 1

        # Добавляем авторов текущего шага для получения авторов, на которых они подписаны
        self.users_for_run = {key: value for key, value in popnitems(self.step, number_for_run) if not (key is None)}
        return

    def make_path(self):
        friends_path = []
        user_id = self.path[self.share_friend][1]
        while user_id is not None:
            friends_path.append({user_id: self.path[user_id][0]})
            user_id = self.path[user_id][1]
        return friends_path

    def make_full_path(self):
        friends_path = self.make_path()
        friends_path.reverse()
        friends_path.append({self.share_friend: self.path[self.share_friend][0]})
        friends_path.extend(self.towards_path.make_path())
        return friends_path

