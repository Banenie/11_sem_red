import csv
import json
import os
import re

from datetime import datetime

class Note():
    def __init__(self, id, title, content, timestamp):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = timestamp


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }


    def view_note(self):
        print(f"\nID: {self.id}\nTitle: {self.title}\nTimestamp: {self.timestamp}")


    def view_note_with_content(self):
        print("-"*40)
        print(f"\nID: {self.id}\nTitle: {self.title}\nContent:\n{self.content}\nTimestamp: {self.timestamp}")
        print("-"*40)


class Task:
    def __init__(self, id, title, description, done, priority, due_date):
        self.id = id
        self.title = title
        self.description = description
        done = str(done)

        if done == "True":
            self.done = "True"
        else:
            self.done = "False"

        self.priority = priority
        self.due_date = due_date
    
    def view_task(self):
        print(f"\nID: {self.id}\nTitle: {self.title}\nDescription: {self.description}\nDone: {self.done}\nPriority: {self.priority}\n Due date: {self.due_date}")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "priority": self.priority,
            "due_date": self.due_date
        }
    

class Contact:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
    
    def view_contact(self):
        print(f"\nID: {self.id}\nName: {self.name}\nPhone: {self.phone}\nemail: {self.email}")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
        }


class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.id = int(id)
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.description = description

    def view_finance(self):
        print(f"\nID: {self.id}\Amount: {self.amount}\nCategory: {self.category}\nDate: {self.date}\nDescription: {self.description}")

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
        }
    

def manage_notes():
    print('\nМеню управления заметками')
    print("1. Создание новой заметки")
    print("2. Просмотр списка заметок")
    print("3. Просмотр подробностей заметки")
    print("4. Редактирование заметки")
    print("5. Экспорт заметок в формате CSV")
    print("6. Импорт заметок в формате CSV")
    print("7. Удаление заметки")
    print("8. Выход")
    
    choice = input("Введите номер действия: ")

    with open('notes.json', 'a+') as file:
        file.seek(0)
        read = file.read()
        if read == '':
            data = []
        else:
            data = json.loads(read)


    if choice == '1':
        try:
            id = data[-1]['id'] + 1
        except IndexError:
            id = 0

        title = input("\nВведите заголовок: ")
        content = input("Введите сожержимое заметки: ")
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        new_note = Note(id, title, content, timestamp)

        with open('notes.json', 'w+') as file:
            json.dump(data + [new_note.to_dict()], file)
        manage_notes()


    elif choice == '2':
        print("-"*40)
        for note in data:
            Note(*note.values()).view_note()
        print("-"*40)
        manage_notes()


    elif choice == '3':
        id = int(input("\nВведите ID заметки: "))
        for note in data:
            if note['id'] == id:
                Note(*note.values()).view_note_with_content()
                break
        manage_notes()


    elif choice == '4':
        id = int(input("\nВведите ID заметки: "))

        new_title = input("\nВведите новый заголовок: ")
        new_content = input("Введите новыое сожержимое заметки: ")
        new_timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        
        for note in range(len(data)):
            if data[note]['id'] == id:
                data[note]['title'] = new_title
                data[note]['content'] = new_content
                data[note]['timestamp'] = new_timestamp

                with open('notes.json', 'w') as file:
                    json.dump(data, file)

                break

        manage_notes()


    elif choice == '5':
        name = input("\nВведите название файла с приставкой .csv: ")

        with open(name, 'w+', encoding='utf-8', newline='') as file:
            a = csv.DictWriter(file, fieldnames=['id', 'title', 'content', 'timestamp'])
            a.writeheader()
            a.writerows(data)
        
        manage_notes()
    

    elif choice == '6':
        name = input("\nВведите название файла без приставки .csv: ")

        with open(name+".csv", 'a+', encoding='utf-8', newline='') as file:
            file.seek(0)
            read = file.read()
            if read == '':
                data = []
            else:
                data = [i for i in csv.DictReader(read.split('\n'))]
                for i in range(len(data)):
                    data[i]['id'] = int(data[i]['id'])
        
        with open('notes.json', 'w') as file:
            json.dump(data, file)

        manage_notes()

    elif choice == '7':
        id = int(input("\nВведите ID заметки: "))
        index = None

        for i in range(len(data)):
            if data[i]['id'] == id:
                index = i
        
        if index is not None:
            data.pop(index)
        
        with open('notes.json', 'w') as file:
            json.dump(data, file)
        
        manage_notes()


    elif choice == '8':
        main_menu()
    else:
        print("\nНеверный ввод. Пожалуйста, выберите правильный пункт.")
        manage_notes()



def manage_tasks():
    print("\nУправление задачами:")
    print("1. Добавить новую задачу")
    print("2. Просмотреть задачи")
    print("3. Отметить задачу как выполненную")
    print("4. Редактировать задачу")
    print("5. Удалить задачу")
    print("6. Экспорт задач в CSV")
    print("7. Импорт задач из CSV")
    print("8. Назад")
    
    choice = input("Выберите действие: ")
    
    with open('tasks.json', 'a+') as file:
        file.seek(0)
        read = file.read()
        if read == '':
            data = []
        else:
            data = json.loads(read)

    if choice == '1':
        try:
            id = data[-1]['id'] + 1
        except IndexError:
            id = 0

        title = input("\nВведите название задачи: ")
        descriprion = input("Введите описание задачи: ")
        done = "False"
        priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")

        while True:
            due_time = input("Введите срок выполнения (в формате ДД-ММ-ГГГГ):")

            matches = re.findall(r"\d\d-\d\d-\d\d\d\d", due_time)
            if len(matches) != 0:
                due_time = matches[0]
                break

        new_task = Task(id, title, descriprion, done, priority, due_time)

        with open('tasks.json', 'w+') as file:
            json.dump(data + [new_task.to_dict()], file)

        manage_tasks()

    elif choice == '2':
        print("-"*40)
        for task in data:
            Task(*task.values()).view_task()
        print("-"*40)

        manage_tasks()
    

    elif choice == '3':
        id = int(input("\nВведите ID задачи: "))
        
        for task in range(len(data)):
            if data[task]['id'] == id:
                data[task]['done'] = "True"

                with open('tasks.json', 'w') as file:
                    json.dump(data, file)

                break

        manage_tasks()
    

    elif choice == '4':
        id = int(input("\nВведите ID задачи: "))

        new_title = input("\nВведите новое название задачи: ")
        new_descriprion = input("Введите новое описание задачи: ")

        new_done = input("Введите сделана ли ваша задача (True/False): ")

        if new_done == "True":
            new_done = "True"
        else:
            new_done = "False"

        new_priority = input("Выберите новый приоритет (Высокий/Средний/Низкий): ")

        while True:
            new_due_date = input("Введите новый срок выполнения (в формате ДД-ММ-ГГГГ):")

            matches = re.findall(r"\d\d-\d\d-\d\d\d\d", new_due_date)
            if len(matches) != 0:
                new_due_time = matches[0]
                break
        
        for task in range(len(data)):
            if data[task]['id'] == id:
                data[task]['title'] = new_title
                data[task]['description'] = new_descriprion
                data[task]["done"] = new_done
                data[task]['priority'] = new_priority
                data[task]['due_date'] = new_due_date

                with open('tasks.json', 'w') as file:
                    json.dump(data, file)

                break

        manage_tasks()


    elif choice == '5':
        id = int(input("\nВведите ID задачи: "))
        index = None

        for i in range(len(data)):
            if data[i]['id'] == id:
                index = i
        
        if index is not None:
            data.pop(index)
        
        with open('tasks.json', 'w') as file:
            json.dump(data, file)
        
        manage_tasks()


    elif choice == '6':
        name = input("\nВведите название файла с приставкой .csv: ")

        with open(name, 'w+', encoding='utf-8', newline='') as file:
            a = csv.DictWriter(file, fieldnames=['id', 'title', 'description', 'done', 'priority', 'due_date'])
            a.writeheader()
            a.writerows(data)
        
        manage_tasks()


    elif choice == '7':
        name = input("\nВведите название файла без приставки .csv: ")

        with open(name+".csv", 'a+', encoding='utf-8', newline='') as file:
            file.seek(0)
            read = file.read()
            if read == '':
                data = []
            else:
                data = [i for i in csv.DictReader(read.split('\n'))]
                for i in range(len(data)):
                    data[i]['id'] = int(data[i]['id'])
        
        with open('tasks.json', 'w') as file:
            json.dump(data, file)

        manage_tasks()

        
    elif choice == '8':
        main_menu()
    else:
        print("\nНеверный ввод. Пожалуйста, выберите правильный пункт.")
        main_menu()


def manage_contacts():
    print("\nУправление контактами:")
    print("1. Добавить новый контакт")
    print("2. Поиск контакта")
    print("3. Редактировать контакт")
    print("4. Удалить контакт")
    print("5. Экспорт контактов в CSV")
    print("6. Импорт контактов из CSV")
    print("7. Назад")
    
    choice = input("Введите номер действия: ")
    
    with open('contacts.json', 'a+') as file:
        file.seek(0)
        read = file.read()
        if read == '':
            data = []
        else:
            data = json.loads(read)


    if choice == '1':
        try:
            id = data[-1]['id'] + 1
        except IndexError:
            id = 0

        name = input("\nВведите имя контакта : ")
        phone = input("Введите номер телефона: ")

        while True:
            email = input("Введите email контакта: ")

            matches = re.findall(r"^\S+@\S+\.\S+$", email)
            if len(matches) != 0:
                email = matches[0]
                break

        new_contact = Contact(id, name, phone, email)

        with open('contacts.json', 'w+') as file:
            json.dump(data + [new_contact.to_dict()], file)

        manage_contacts()


    elif choice == '2':
        s = input("Введите имя или телефон контакта: ")
        
        for i in range(len(data)):
            if data[i]['name'] == s or data[i]['phone'] == s:
                print('-'*40)
                Contact(*data[i].values()).view_contact()
                print('-'*40)
                break

        manage_contacts()


    elif choice == '3':
        id = int(input("\nВведите ID контакта: "))

        new_name = input("\nВведите новое имя: ")
        new_phone = input("Введите новоый телефон: ")

        while True:
            new_email = input("Введите новый email контакта: ")

            matches = re.findall(r"^\S+@\S+\.\S+$", new_email)
            if len(matches) != 0:
                new_email = matches[0]
                break
        
        for contact in range(len(data)):
            if data[contact]['id'] == id:
                data[contact]['name'] = new_name
                data[contact]['phone'] = new_phone
                data[contact]["email"] = new_email

                with open('contacts.json', 'w') as file:
                    json.dump(data, file)

                break

        manage_contacts()
    elif choice == '4':
        id = int(input("\nВведите ID контакта: "))
        index = None

        for i in range(len(data)):
            if data[i]['id'] == id:
                index = i
        
        if index is not None:
            data.pop(index)
        
        with open('contacts.json', 'w') as file:
            json.dump(data, file)
        
        manage_contacts()


    elif choice == '5':
        file_name = input("\nВведите название файла с приставкой .csv: ")

        with open(file_name, 'w+', encoding='utf-8', newline='') as file:
            a = csv.DictWriter(file, fieldnames=['id', 'name', 'phone', 'email'])
            a.writeheader()
            a.writerows(data)
        
        manage_contacts()

    elif choice == '6':
        name = input("\nВведите название файла без приставки .csv: ")

        with open(name+".csv", 'a+', encoding='utf-8', newline='') as file:
            file.seek(0)
            read = file.read()
            if read == '':
                data = []
            else:
                data = [i for i in csv.DictReader(read.split('\n'))]
                for i in range(len(data)):
                    data[i]['id'] = int(data[i]['id'])
        
        with open('contacts.json', 'w') as file:
            json.dump(data, file)

        manage_tasks()
    

    elif choice == '7':
        main_menu()
    else:
        print("\nНеверный ввод. Пожалуйста, выберите правильный пункт.")
        main_menu()


def manage_finances():
    print("\nУправление финансовыми записями:")
    print("1. Добавить новую запись")
    print("2. Просмотреть все записи")
    print("3. Генерация отчёта")
    print("4. Удалить запись")
    print("5. Экспорт финансовых записей в CSV")
    print("6. Импорт финансовых записей из CSV")
    print("7. Назад")
    
    choice = input("Введите номер действия: ")
    
    with open('finances.json', 'a+') as file:
        file.seek(0)
        read = file.read()
        if read == '':
            data = []
        else:
            data = json.loads(read)
    
    if choice == '1':
        try:
            id = data[-1]['id'] + 1
        except IndexError:
            id = 0

        amount = input("\nВведите количество: ")
        category = input("Введите категорию: ")

        while True:
            date = input("Введите срок выполнения (в формате ДД-ММ-ГГГГ):")

            matches = re.findall(r"\d\d-\d\d-\d\d\d\d", date)
            if len(matches) != 0:
                date = matches[0]
                break
        
        descriprion = input("Введите описание: ")

        new_task = FinanceRecord(id, amount, category, date, descriprion)

        with open('finances.json', 'w+') as file:
            json.dump(data + [new_task.to_dict()], file)


        manage_finances()


    elif choice == '2':
        print("-"*40)
        for finance in data:
            FinanceRecord(*finance.values()).view_finance()
        print("-"*40)

        manage_finances()


    elif choice == '3':
        a = 0
        b = 0

        for i in range(len(data)):
            if int(data[i]['amount']) > 0:
                a += int(data[i]['amount'])
            elif int(data[i]['amount']) < 0:
                b += int(data[i]['amount'])

        print(f"Финансовый отчёт за период: {data[0]['date']}-{data[-1]['date']}")
        print(f'- Общий доход: {a} руб.')
        print(f'- Общие расходы: {b*(-1)} руб.')
        print(f'- Баланс: {a + b} руб.')
        print(f'Подробная информация сохранена в файле report-{data[0]["date"]}-{data[-1]["date"]}.csv')

        file_name = f'report-{data[0]["date"]}-{data[-1]["date"]}.csv'

        with open(file_name, 'w+', encoding='utf-8', newline='') as file:
            a = csv.DictWriter(file, fieldnames=['id', 'amount', 'category', 'date', 'description'])
            a.writeheader()
            a.writerows(data)

        manage_finances()


    elif choice == '4':
        id = int(input("\nВведите ID отчета: "))
        index = None

        for i in range(len(data)):
            if data[i]['id'] == id:
                index = i
        
        if index is not None:
            data.pop(index)
        
        with open('finances.json', 'w') as file:
            json.dump(data, file)

        manage_finances()
    

    elif choice == '5':
        file_name = input("\nВведите название файла с приставкой .csv: ")

        with open(file_name, 'w+', encoding='utf-8', newline='') as file:
            a = csv.DictWriter(file, fieldnames=['id', 'amount', 'category', 'date', 'description'])
            a.writeheader()
            a.writerows(data)

        manage_finances()
    

    elif choice == '6':
        name = input("\nВведите название файла без приставки .csv: ")

        with open(name+".csv", 'a+', encoding='utf-8', newline='') as file:
            file.seek(0)
            read = file.read()
            if read == '':
                data = []
            else:
                data = [i for i in csv.DictReader(read.split('\n'))]
                for i in range(len(data)):
                    data[i]['id'] = int(data[i]['id'])
        
        with open('finances.json', 'w') as file:
            json.dump(data, file)

        manage_finances()
    elif choice == '7':
        main_menu()
    else:
        print("\nНеверный ввод. Пожалуйста, выберите правильный пункт.")
        manage_finances()


def calculator():
    inp = input("Введите выражение: ")
    if inp != '':
        print(eval(inp))

        calculator()
    main_menu()


def exit_app():
    print("\nДо свидания! Спасибо за использование нашего помощника.")


def main_menu():
    print("\nДобро пожаловать в Персональный помощник!")
    print("1. Управление заметками")
    print("2. Управление задачами")
    print("3. Управление контактами")
    print("4. Управление финансовыми записями")
    print("5. Калькулятор")
    print("6. Выход")
    
    choice = input("Введите номер действия: ")
    
    if choice == '1':
        manage_notes()
    elif choice == '2':
        manage_tasks()
    elif choice == '3':
        manage_contacts()
    elif choice == '4':
        manage_finances()
    elif choice == '5':
        calculator()
    elif choice == '6':
        exit_app()
    else:
        print("\nНеверный ввод. Пожалуйста, выберите правильный пункт.")
        main_menu()
        

main_menu()
