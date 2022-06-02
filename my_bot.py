import sys
import telebot
from types import NoneType

BOT_TOKEN = 'token'
bot = telebot.TeleBot(BOT_TOKEN)

Users_list = []

#Когда пользователь вводит текст, идёт проверка: есть ли он в списке юзеров.
@bot.message_handler(content_types=["text"])
def check_id(message):
    if message.from_user.id in Users_list:
        enter_expression(message)
    else:
        Users_list.append(message.from_user.id)
        send_welcome(message)

# Функцию кидает приветственный месседж с описанием что этот бот такое.
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi. This is a test calculator for QA purposes. First of all we need to authorize. Please, enter a password:")
    bot.register_next_step_handler(message, check_password)

# Проверка пароля
def check_password(message):
    while message.text != "password":
        bot.send_message(message.chat.id, "That's incorrect password, try again.")
        bot.register_next_step_handler(message, check_password)
        break
    else:
        disclaimer(message)

# Предупреждение, что можно вводить, а что - нет.
def disclaimer(message):
    bot.send_message(message.chat.id, "Don't use any letters, multiple operators.\nNumbers and operators only!")
    enter_expression(message)

# Просит пользователя ввести математическое выражение.
def enter_expression(message):
    bot.send_message(message.chat.id, "Please, enter any math expression:")
    bot.register_next_step_handler(message, check_NoneType)

# Проверка не является ли текст NoneType.
def check_NoneType(message):
    if type(message.text) == NoneType:
        bot.send_message(message.chat.id,"Don't use NoneType input!")
        bot.register_next_step_handler(message, check_NoneType)
    else:
        check_doubles(message)

# Проверка нет ли в стринге повторяющихся символов / операторов.
def check_doubles(message):
    for element in range(len(message.text)):
        if (element != 0) and (message.text[element] == message.text[element - 1]) and (message.text.isdigit() == False):
            bot.send_message(message.chat.id, "Don't use multiple operators or symbols!")
            bot.register_next_step_handler(message, check_NoneType)
            sys.exit()

    eval_operation(message)
 
# Логика для вычисление математического выражения.
def eval_operation(message):
    try:
        result = eval(message.text)
        round_result = round(result, 10)
    except SyntaxError:
        bot.send_message(message.chat.id,"Invalid input expression syntax!")
        bot.register_next_step_handler(message, check_NoneType)
    except ZeroDivisionError:
        bot.send_message(message.chat.id,"Division by zero is bad!")
        bot.register_next_step_handler(message, check_NoneType)
    except NameError:
        bot.send_message(message.chat.id,"Don't use letters!")
        bot.register_next_step_handler(message, check_NoneType)
    else:
        bot.send_message(message.chat.id, round_result)
        bot.register_next_step_handler(message, check_NoneType)

bot.infinity_polling()