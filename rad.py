import os
import json
from telethon import TelegramClient
import time

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

accounts = config['accounts']
print("Total account: " + str(len(accounts)))
folder_session = 'session/'

# login
clients = []
for account in accounts:
    api_id = account['api_id']
    api_hash = account['api_hash']
    phone = account['phone']

    client = TelegramClient(folder_session + phone, api_id, api_hash)

    client.connect()

    if client.is_user_authorized():
        print(phone + ' login success')
        clients.append({
            'phone': phone,
            'client': client
        })
        time.sleep(1)
    else:
        print(phone + ' login fail')


# group target
group_target_id = config['group_target']
# group source
group_source_id = config['group_source']
root_path = os.path.abspath(os.curdir)

# filter clients


def filterus():
    for my_client in clients:
        phone = my_client['phone']
        path_group = root_path + '/data/group/' + phone + '.json'
        path_group2 = root_path + '/data/filteruser/' + \
            phone + "_" + str(group_source_id) + '.json'
        if os.path.isfile(path_group):
            json2 = root_path + '/data/user/' + \
                phone + "_" + str(group_source_id) + '.json'
            json1 = root_path + '/data/user/' + \
                phone + "_" + str(group_target_id) + '.json'
            with open(json1) as f:
                json11 = json.loads(f.read())
            with open(json2) as b:
                json22 = json.loads(b.read())

            newjson = [user for user in json22 if not any(
                user["user_id"] == other["user_id"] for other in json11)]
            with open(path_group2, "w") as f:
                json.dump(newjson, f, ensure_ascii=False, indent=4)
            #disconect
            client.disconnect()
            time.sleep(2)
        else:
           print("couldn't filter all account try later or use python add_member.py")



filterus()