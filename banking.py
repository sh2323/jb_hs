import random
import sqlite3 as sql

conn = sql.connect('card.s3db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS  card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()

start_menu = """1. Create an account
2. Log into account
0. Exit"""
login_menu = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
"""


def luhn_alg(card_id):
    sum = 0

    for i in range(len(card_id)):
        if i % 2 == 0:
            el = int(card_id[i]) * 2
            if el > 9:
                el -= 9
        else:
            el = int(card_id[i])
        sum += el
    if sum % 10 != 0:
        check_sum = 10 - sum % 10
    else:
        check_sum = 0
    return card_id + str(check_sum)


def select_query(log_in, column):
    cur.execute(f"""SELECT {column} 
                      FROM card 
                     WHERE number = {log_in}""")
    return cur.fetchone()


def update_query(val, log):
    cur.execute(f"""UPDATE card SET 
                         balance = balance + {val} 
                   WHERE number = {log}""")
    conn.commit()


def create_acc():
    user_data = dict()
    id_pin = {}
    db_id = random.randint(0, 9999999)
    ID = '400000'
    acc_id = str(random.randint(100000000, 999999999))
    pin_code = str(random.randint(1000, 9999))
    id_pin[pin_code] = db_id

    user_data[pin_code] = luhn_alg(ID + acc_id)
    print('\nYour card has been created')
    print(f'Your card number:\n{user_data[pin_code]}')
    print(f'Your card PIN:\n{pin_code}')
    print()
    cur.execute(f"INSERT INTO card VALUES ({db_id}, {user_data[pin_code]}, {pin_code}, 0)")
    conn.commit()


def balance(login):
    sel_balance = select_query(login, 'balance')
    print('\nBalance:', *sel_balance, '\n')


def add_income(login):
    income = int(input('\nEnter income:\n'))
    update_query(income, login)
    print('Income was added!\n')


def do_transfer(login):
    acc_num = input('\nTransfer\nEnter card number:\n')
    sel_acc = select_query(acc_num, 'number')

    if acc_num == login:
        print("You can't transfer money to the same account!\n")
    elif acc_num != luhn_alg(acc_num[:len(acc_num) - 1]):
        print("Probably you made mistake in the card number. Please try again!\n")
    elif sel_acc is None:
        print("Such a card does not exist.\n")
    else:
        money = int(input("Enter how much money you want to transfer:\n"))
        sel_transfer = select_query(login, 'balance')

        if money > int(*sel_transfer):
            print('Not enough money!\n')
        else:
            update_query(money, acc_num)
            update_query(-money, login)
            print("Success!\n")


def close_acc(log, pas):
    print("\nThe account has been closed!\n")
    cur.execute(f"DELETE FROM card WHERE number = {log} AND pin = {pas}")
    conn.commit()


def log_into_acc():
    login = input('\nEnter your card number:\n')
    pin = input('Enter your PIN:\n')
    cur.execute(f"""SELECT number 
                      FROM card 
                     WHERE number = {login}
                     AND   pin = {pin}""")
    if cur.fetchone() is None:
        print('\nWrong card number or PIN!\n')
    else:
        print('\nYou have successfully logged in!\n')
        while True:
            user_inp = int(input(login_menu))
            if user_inp == 1:
                balance(login)
            if user_inp == 2:
                add_income(login)
            if user_inp == 3:
                do_transfer(login)
            if user_inp == 4:
                close_acc(login, pin)
                break
            if user_inp == 5:
                print('\nYou have successfully logged out!\n')
                break
            if user_inp == 0:
                print('\nBye!')
                return 0


def main():
    while True:
        print(start_menu)
        user_input = int(input())
        if user_input == 1:
            create_acc()
        if user_input == 2:
            if log_into_acc() == 0:
                break
        if user_input == 0:
            print('\nBye!')
            break


if __name__ == '__main__':
    main()
