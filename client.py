import sqlite3
from functions import *


def registration(mail, password, login):
    def duplicate(mail):
        base = sqlite3.connect('sqlbase')
        cur = base.cursor()
        table = cur.execute("""SELECT mail FROM players""")
        table = [i[0] for i in table]
        if mail in table:
            base.close()
            return False
        base.close()
        return True

    def chek1(mail):
        if '@' not in mail or '.' not in mail:
            return False
        if mail.index('.') - mail.index('@') < 2 or mail.index('@') == 0 or mail.index('.') + 1 == len(mail):
            return False
        for i in mail:
            if (i != '!' and not i.isalpha() and i != '@' and not i.isdigit() and i != '.' or mail.count('@') > 1 or
                    mail.count('.') > 1):
                return False
        return True

    def chek2(password):
        if len(password) < 8:
            return False
        return True

    if duplicate(mail) and chek1(mail) and chek2(password):
        base = sqlite3.connect('sqlbase')
        cur = base.cursor()
        cur.execute("""INSERT INTO players (mail, password, login, settings) VALUES 
                        (?, ?, ?, ?)""", [mail, password, login, ''])
        base.commit()
        base.close()
        return 'Успешно'
    elif not duplicate(mail):
        return 'Почта уже есть'
    elif not chek1(mail):
        return 'Почта бяка'
    else:
        return 'Короткий пароль'


def vhod(mail, password):
    base = sqlite3.connect('sqlbase')
    cur = base.cursor()
    information = cur.execute("""SELECT * FROM players""")
    information = [[str(i[0]), str(i[1]), str(i[2])] for i in information]
    inf1 = [[str(i[0]), str(i[1])] for i in information]
    inf2 = [[str(i[2]), str(i[1])] for i in information]
    if [mail, password] not in inf1 and [mail, password] not in inf2:
        if mail not in [i[0] for i in inf1] and mail not in [i[0] for i in inf2]:
            return 'Пользователь не найден'
        else:
            return 'Пароль неверный'
    else:
        if [mail, password] in inf1:
            flag = inf1.index([mail, password])
        else:
            flag = inf2.index([mail, password])
        set_param_in_client("user", information[flag][2])
    return "Успешно"


def get_client_name():
    return get_param_from_client("user")


def razlogin():
    set_param_in_client("user", "None")
