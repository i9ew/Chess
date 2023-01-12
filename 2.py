import sqlite3


mail, password, login = input(), input(), input()


def duplicate(mail):
    base = sqlite3.connect('sqlbase')
    cur = base.cursor()
    table = cur.execute("""SELECT mail FROM players""")
    table = [i[0] for i in table]
    if mail in table:
        base.close()
        print('Почта занята')
        return False
    base.close()
    return True


def chek(mail):
    if '@' not in mail or '.' not in mail:
        print('Введите почту')
        return False
    if mail.index('.') - mail.index('@') < 2 or mail.index('@') == 0 or mail.index('.') + 1 == len(mail):
        print('Введите почту')
        return False
    for i in mail:
        if (i != '!' and not i.isalpha() and i != '@' and not i.isdigit() and i != '.' or mail.count('@') > 1 or
                mail.count('.') > 1):
            print('Введите почту')
            return False
    if len(password) < 8:
        print('Плохой пароль')
        return False
    return True


def registration(mail, password, login):
    if duplicate(mail) and chek(mail):
        base = sqlite3.connect('sqlbase')
        cur = base.cursor()
        cur.execute("""INSERT INTO players (mail, password, login, settings) VALUES 
                        (?, ?, ?, ?)""", [mail, password, login, ''])
        base.commit()
        base.close()
        print('Успешно')


def vhod(mail, password):
    base = sqlite3.connect('sqlbase')
    cur = base.cursor()
    information = cur.execute("""SELECT * FROM players""")
    information = [[str(i[0]), str(i[1]), str(i[2])] for i in information]
    inf1 = [[str(i[0]), str(i[1])] for i in information]
    inf2 = [[str(i[2]), str(i[1])] for i in information]
    if [mail, password] not in inf1 and [mail, password] not in inf2:
        print('Пользователь не найден')
    else:
        if [mail, password] in inf1:
            flag = inf1.index([mail, password])
        else:
            flag = inf2.index([mail, password])
        with open('username.txt', 'w') as f:
            print(f'user={information[flag][2]}', file=f)


def razlogin():
    with open('username.txt', 'w') as f:
        print(f'user=None', file=f)


vhod(mail, password)
