from bs4 import BeautifulSoup as bs
import requests
from collections import defaultdict

# Getting last_page to continue parsing.
with open('last.txt', 'r') as file:
    last_page = int(file.read())

# manga list
X = ["Возвращение железнокровной гончей",
     "Безграничный маг",
     "Младший сын мастера меча",
     "Чёртова реинкарнация",
     "Выбери меня!",
     "Прирожденный наёмник",
     "Возрождение Хуашань",
     "Наномашины",
     "Король-рыцарь, вернувшийся с богом",
     "Переродившийся убийца — гений фехтования",
     "Элисед",
     "Гениальный маг, пожирающий лекарства",
     "Фермерство в башне в одиночку",
     "Возвращение темного мага",
     "Гениальный Мечник Академии",
     "Это и вправду герой?",
     "Жнец дрейфующей Луны",
     "Игрок скрывает прошлое",
     "Волшебник, пожирающий драконов"]


collection = defaultdict(list)
loop = True

while loop:
    temp = []   # Temporary list
    last_page_url = str(last_page)
    url = "https://t.me/s/lnmanga?after=" + last_page_url
    r = requests.get(url)

    soup = bs(r.content, 'lxml')

    content = soup.find_all(class_="tgme_widget_message_wrap")

    for message in content:
        temp.append(message)
        msg = message.find(class_="tgme_widget_message")
        id = msg.get("data-post")[8:]
        text = msg.find(class_="tgme_widget_message_text")
        s = str(text)
        result = s.split('<br/>')[0]
        name = result.split('>')[1]
        try:
           tag_result = s.split('<br/>')[1]
        except IndexError:
           tag_result = None # or any other default value
        link = text.find_all("a")
        try:
           href = link[1].get("href")
        except IndexError:
           href = None # or any other default value
        if name in X:
            collection[name].append([tag_result, href])
        print(id)

    # Checking end of page
    if len(temp) < 20:
        loop = False
    else:
        last_page += len(temp)
    print(last_page)

# Saving last page
with open('last.txt', 'w') as file:
    file.write(str(last_page))

# Printing all collection info
print()
for keys, values in collection.items():
    print(keys)
    for val in values:
        print(val)
    print()
