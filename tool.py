from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()
correct_answers = dict()


class FlashCards(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    answer = Column(String)
    question = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main_menu():
    while True:
        print('1. Add flashcards', '2. Practice flashcards', '3. Exit', sep='\n')
        user_inp = input()

        if user_inp == '1':
            add_menu()

        elif user_inp == '2':
            if len(session.query(FlashCards).all()) == 0:
                print('\nThere is no flashcard to practice!\n')

            else:
                practice_menu()

        elif user_inp == '3':
            print('\nBye!')
            exit()

        else:
            print(f'\n{user_inp} is not an option\n')


def add_menu():
    while True:
        print('\n1. Add a new flashcard\n2. Exit')
        add_input = input()
        print()

        if add_input == '1':
            while True:
                question = input('Question:\n')
                if question:
                    break

            while True:
                answer = input('Answer:\n')
                if answer:
                    break
                print()

            new_data = FlashCards(question=question, answer=answer)
            session.add(new_data)
            session.commit()

        elif add_input == '2':
            main_menu()

        else:
            print(f'{add_input} is not an option')


def practice_menu():
    result_list = session.query(FlashCards).all()
    n = 0
    flag = 0

    while n < len(result_list):
        if flag == 0:
            print('\nQuestion:', result_list[n].question)

        print('''press "y" to see the answer:
press "n" to skip:
press "u" to update:''')
        user_ans = input()

        if user_ans == 'y' or user_ans == 'n':
            if result_list[n].answer not in correct_answers:
                correct_answers[result_list[n].answer] = 0

            if user_ans == 'y':
                print('Answer:', result_list[n].answer)

            while True:
                print('''press "y" if your answer is correct:
press "n" if your answer is wrong:''')

                is_correct = input()

                if is_correct == 'y' or is_correct == 'n':
                    if is_correct == 'y':
                        correct_answers[result_list[n].answer] += 1

                        if correct_answers[result_list[n].answer] == 3:
                            session.delete(result_list[n])
                            session.commit()
                    break

                else:
                    print(is_correct, 'is not an option')

        elif user_ans == 'u':
            while True:
                print('''press "d" to delete the flashcard:
press "e" to edit the flashcard:''')
                user_choice = input()

                if user_choice == 'd' or user_choice == 'e':
                    if user_choice == 'd':
                        session.delete(result_list[n])

                    elif user_choice == 'e':
                        print('\ncurrent question:', result_list[n].question)
                        print('please write a new question:')
                        q = input()

                        if not q:
                            q = result_list[n].question

                        print('current answer:', result_list[n].answer)
                        print('please write a new answer:')
                        a = input()

                        if not a:
                            a = result_list[n].answer

                        result_list[n].question = q
                        result_list[n].answer = a

                    session.commit()
                    break

                else:
                    print(user_choice, 'is not an option')

        else:
            print(user_ans, 'is not an option')
            flag = 1
            continue

        n += 1
        flag = 0

    print()
    main_menu()


main_menu()
