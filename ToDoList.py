from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
menu = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit"""

rows = session.query(Table).all()
today = datetime.today()
weekdays = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}


def task_output(str1, str2, rws):
    count = 1
    print(str1)
    if len(rws) == 0:
        print(str2)
    for row in rws:
        print(f"{count}. {row}. {row.deadline.day} {row.deadline.strftime('%b')}")
        count += 1


while True:
    print(menu)
    user_input = input()
    rows = session.query(Table).all()
    if user_input == '1':
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if len(rows) == 0:
            print(f"\nToday {today.day} {today.strftime('%b')}:\nNothing to do!\n")
        else:
            print(f"\nToday {today.day} {today.strftime('%b')}:")
            for row in range(len(rows)):
                print(f'{row+1}. {rows[row]}')
            print()
    if user_input == '2':
        for i in range(7):
            date = today.date() + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == date).all()
            if len(rows) == 0:
                print(f"\n{weekdays[date.weekday()]} {date.day} {date.strftime('%b')}:\nNothing to do!")
            else:
                print(f"\n{weekdays[date.weekday()]} {date.day} {date.strftime('%b')}:")
                for row in range(len(rows)):
                    print(f'{row + 1}. {rows[row]}')
        print()
    if user_input == '3':
        string1 = '\nAll tasks:'
        string2 = 'Nothing to do'
        rows = session.query(Table).order_by(Table.deadline).all()
        task_output(string1, string2, rows)
        print()

    if user_input == '4':
        string1 = '\nMissed tasks:'
        string2 = 'Nothing is missed'
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        task_output(string1, string2, rows)
        print()

    if user_input == '5':
        day = input('\nEnter task\n')
        print('Enter deadline')
        deadl = list(map(int, input().split('-')))
        new_row = Table(task=day, deadline=datetime(deadl[0], deadl[1], deadl[2]))
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')

    if user_input == '6':
        string1 = '\nChoose the number of the task you want to delete:'
        string2 = 'Nothing to delete'
        rows = session.query(Table).order_by(Table.deadline).all()
        task_output(string1, string2, rows)
        index = int(input()) - 1
        if index >= len(rows):
            continue
        specific_row = rows[index]  # in case rows is not empty
        session.delete(specific_row)
        session.commit()
        print('The task has been deleted!\n')

    if user_input == '0':
        print('\nBye!')
        break
