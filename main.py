import telebot
from myignor import bot_token


# Шлях до файлу зі списком чорних слів
blacklist_file = 'blacklist.txt'


# Ініціалізація бота
bot = telebot.TeleBot(bot_token)


# Функція для завантаження списку людей з файлу
def load_blacklist():
    try:
        with open(blacklist_file, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


# Функція для зберігання списку людей і авто у файлі
def save_blacklist (blacklist):
    with open(blacklist_file, 'w') as file:
        file.write('\n'.join(blacklist))


# Завантаження чорного списку при запуску бота
blacklist = load_blacklist()


# Обробник команди для додавання імені до чорного списку
@bot.message_handler (commands=['add'])
def add_word_to_blacklist(message):
    word = message.text.split(maxsplit=1)[1].lower()
    if word not in blacklist:
        blacklist.append(word)
        save_blacklist(blacklist)
        bot.reply_to(message, f" '{word}' додано до чорного списку.")
    else:
        bot.reply_to(message, f" '{word}' вже є в чорному списку.")
    # Оновлення чорного списку або збереження у файл, якщо потрібно
    # Наприклад, можна зберегти слово у файлі blacklist.txt:
    with open('blacklist.txt', 'a') as f:
        f.write(word + '\n')


# Обробник команди для видалення слова з чорного списку
@bot.message_handler(commands=['dell'])
def remove_word_from_blacklist(message):
    word = message.text.split(maxsplit=1)[1].lower()
    if word in blacklist:
        blacklist.remove(word)
        save_blacklist(blacklist)
        bot.reply_to(message, f"Слово '{word}' видалено з чорного списку.")


# Обробник команди для видалення всіх слів зі списку
@bot.message_handler(commands=['clear'])
def clear_blacklist(message):
    blacklist.clear()
    save_blacklist(blacklist)
    bot.reply_to(message, "Всі слова з чорного списку видалено.")


# Обробник команди для виведення чорного списку
@bot.message_handler(commands=['show'])
def show_blacklist(message):
    if blacklist:
        bot.reply_to(message, '\n'.join(blacklist))


# Функція для перевірки повідомлення на наявність співпадінь
def check_blacklist(message_text):
    matches = []
    for word_pair in blacklist:
        words = word_pair.split()
        if all(word.lower() in message_text.lower() for word in words):
            matches.append(word_pair)
    return matches if matches else None


# Обробник повідомлень з ключовим словом "привіт"
@bot.message_handler(func=lambda message: "привіт" in message.text.lower())
def handle_hello(message):
    bot.reply_to(message, "привіт!"
                          " я телеграм бот автоматизатор чорного списку,  введи /help, щоб побачити функції")


# Обробник повідомлень з ключовим словом "привіт"
@bot.message_handler(func=lambda message: "інструкція" in message.text.lower())
def handle_hello(message):
    bot.reply_to(message, "щоб ти зміг коректно додавати в чорний список або видаляти,\n"
                          "обов'язково потрібно написати  /  після нього потрібне ключове слово\n"
                          "наприклад /add імя фалілія\n")


# Обробник команди для відображення списку команд
@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = "Список доступних команд:\n"
    help_text += "/add <слово1 слово2> - додати слово або пару слів до чорного списку\n"
    help_text += "/dell <слово1 слово2> - видалити слово або пару слів з чорного списку\n"
    help_text += "/show - показати усі слова з чорного списку\n"
    bot.reply_to(message, help_text)


# Обробник усіх повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Перевіряємо повідомлення на наявність чорних слів
    blacklisted_word = check_blacklist(message.text)
    if blacklisted_word:
        bot.reply_to(message, f"ЗНАЙДЕНО ЗБІГ З ЧОРНИМ СПИСКОМ!!!!: {blacklisted_word}")


# Запуск бота
bot.polling(none_stop=True)
