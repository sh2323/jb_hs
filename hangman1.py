import random


def hangman(count, letters, result):
    while True:
        print()
        print(*result, sep='')
        guess = input("Input a letter: ")
        check = guess.islower()
        if guess in letters:
            print('You already typed this letter')
            continue
        if len(guess) != 1:
            print('You should input a single letter')
            continue
        if not check:
            print('It is not an ASCII lowercase letter')
            continue

        letters += guess
        if guess in random_word:
            if guess not in result:
                for letter_num in range(len(random_word)):
                    if guess == random_word[letter_num]:
                        result[letter_num] = guess
            else:
                print('No improvements')
                count -= 1
        else:
            print('No such letter in the word')
            count -= 1
        if '-' not in result:
            print('\n', *result, sep='')
            print('You guessed the word!')
            print('You survived!\n')
            break
        if count == 0:
            print('You are hanged!\n')
            break


print("H A N G M A N")
while True:
    choice = input('Type "play" to play the game, "exit" to quit: ')
    if choice == 'play':
        lives = 8
        letter = str()
        words = ['python', 'java', 'kotlin', 'javascript']
        random_word = random.choice(words)
        res = list(len(random_word) * '-')
        hangman(lives, letter, res)
    else:
        break
