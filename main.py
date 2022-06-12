from Bot import Bot

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
