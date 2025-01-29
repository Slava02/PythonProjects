import random
import game_settings

def main():
    print("Добро пожаловать в игру 'Виселица'!")
    while True:
        choice = input("Начать новую игру? (да/нет): ").lower()
        if choice == 'нет':
            print("Спасибо за игру! До свидания!")
            break
        elif choice == 'да':
            start_game()
        else:
            print("Некорректный ввод. Пожалуйста, введите 'да' или 'нет'.")

def start_game():
    print("Начинаем новую игру!")
    word = {letter: False for letter in select_word(load_words())}
    trials = set()
    while True:
        display(word, trials)
        make_guess(word, trials)

        if len(trials) >= len(game_settings.gallows_states):
            print("Вы проиграли! Ответ:")
            print(key for key in word.keys())
            return

        if all(value for value in word.values()):
            print("Вы выиграли!")
            return


def display(word, trials):
    for hangman in game_settings.gallows_states[len(trials)]:
        print(hangman)
    print([key if value else '_' for key, value in word.items()])
    print(f'Уже пробовали: {trials}\n' if len(trials) > 0 else '', end='')

def make_guess(word, trials):
    while True:
        guess = input("Введите букву: ").lower()
        is_valid, message = validate_input(guess, trials)

        if not is_valid:
            print(message)
            continue

        break

    if guess in word:
        word[guess] = True
    else:
        trials.add(guess)

def validate_input(letter, trials):
    if len(letter) != 1:
        return False, "Пожалуйста, введите только одну букву."
    if not letter.isalpha() or letter not in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
        return False, "Пожалуйста, введите букву русского алфавита."
    if letter in trials:
        return False, "Эта буква уже была угадана."
    return True, ""


def load_words():
    with open("words.txt", "r", encoding="utf-8") as file:
        return [line.strip() for line in file]

def select_word(words):
    """
    Выбирает случайное слово из файла words.txt с заданным количеством букв.
    Запрашивает у пользователя количество букв и проверяет его корректность.
    """
    while True:
        try:
            letters_num = int(input("Введите количество букв: "))
            if not (game_settings.min_word_len <= letters_num <= game_settings.max_word_len):
                print("Количество букв должно быть от {} до {}".format(
                    game_settings.min_word_len, game_settings.max_word_len))
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число.")

    num_words = []
    for word in words:
        if len(word) == letters_num:
            num_words.append(word)

    if not num_words:
        print("Нет слов с такой длиной в словаре. Попробуйте еще раз")
        return select_word(words)

    return random.choice(num_words)


if __name__ == "__main__":
    main()





