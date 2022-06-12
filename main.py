import vk_api  # использование VK API
from vk_api.utils import get_random_id
import os
from config import *

class Bot:
    """
    Базовый класс бота ВКонтакте
    """

    # текущая сессия ВКонтакте
    vk_session = None

    # доступ к API ВКонтакте
    vk_api_access = None

    # пометка авторизованности
    authorized = False

    # id пользователя ВКонтакте (например, 1234567890) в виде строки
    # можно использовать, если диалог будет вестись только с конкретным человеком
    default_user_id = None

    def __init__(self):
        """
        Инициализация бота при помощи получения доступа к API ВКонтакте
        """

        # авторизация
        self.vk_api_access = self.do_auth()

        if self.vk_api_access is not None:
            self.authorized = True

        # получение id пользователя из файла настроек окружения .env в виде строки USER_ID="1234567890"
        self.default_user_id = USER_ID


    def do_auth(self):
        """
        Авторизация за пользователя (не за группу или приложение)
        Использует переменную, хранящуюся в файле настроек окружения .env в виде строки ACCESS_TOKEN="1q2w3e4r5t6y7u8i9o..."
        :return: возможность работать с API
        """
        token = ACCESS_TOKEN
        try:
            self.vk_session = vk_api.VkApi(token=token)
            return self.vk_session.get_api()
        except Exception as error:
            print(error)
            return None

    def send_message(self, receiver_user_id: str = None, message_text: str = "тестовое сообщение"):
        """
        Отправка сообщения от лица авторизованного пользователя
        :param receiver_user_id: уникальный идентификатор получателя сообщения
        :param message_text: текст отправляемого сообщения
        """
        if not self.authorized:
            print("Unauthorized. Check if ACCESS_TOKEN is valid")
            return

        # если не указан ID - берём значение по умолчанию, если таковое указано в .env-файле
        if receiver_user_id is None:
            receiver_user_id = self.default_user_id

        try:
            self.vk_api_access.messages.send(user_id=receiver_user_id, message=message_text, random_id=get_random_id())
            print(f"Сообщение отправлено для ID {receiver_user_id} с текстом: {message_text}")
        except Exception as error:
            print(error)

    def getDialogsList(self):
        try:
            dialogs = self.vk_api_access.messages.getConversations()
        except Exception as error:
            print(error)
        return list(map(self.normalyzeUsers, dialogs['items']))

    def getUserInfo(self, user_id):
        return self.vk_api_access.users.get(user_id=user_id)

    def normalyzeUsers(self, item):
        if item['conversation']['peer']['type']=='chat':
            return item['conversation']['peer'], item['conversation']['chat_settings']['title']
        if item['conversation']['peer']['type']=='user':
            userInfo = self.getUserInfo(user_id = item['conversation']['peer']['id'])[0]
            return item['conversation']['peer'], userInfo['first_name'], userInfo['last_name']

    def getMesssagesNum(self, id):
        return self.vk_api_access.messages.getHistory(user_id=id)['items'][0]['conversation_message_id']

    def getMessage(self, id, peerId):
        return self.vk_api_access.messages.getByConversationMessageId(peer_id=peerId, conversation_message_ids=id)


if __name__ == '__main__':
    bot = Bot()
    dialogs = bot.getDialogsList()

    for i, dialog in enumerate(dialogs):
        print(i+1, dialog)

    statistics = {}
    index = int(input("Input chat number: "))
    id=dialogs[index-1][0]['id']
    messagesnum = bot.getMesssagesNum(id=id)
    print("==========================================================")
    print()
    try:
        for messagenum in range(messagesnum):
            messageItems = bot.getMessage(id=messagenum+1, peerId=id)['items']
            if len(messageItems)>0:
                message = messageItems[0]
                name = bot.getUserInfo(message['from_id'])[0]['first_name']
                print(bot.getUserInfo(message['from_id'])[0]['first_name']+':', message['text'])
                if name in statistics.keys():
                    statistics[name]+=1
                else:
                    statistics[name]=1
    except:
        pass
    print()
    print(statistics)
    #bot.send_message()
#{'Константин': 659, 'София': 1773, 'Екатерина': 790}
