from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# Кнопки со всеми продуктами(основное меню)
def main_menu(get_pr_name_id):
    # Создаем пространство для кнопок
    buttons = InlineKeyboardMarkup(row_width=2)

    # Создаем кнопки (несгорамые)
    order = InlineKeyboardButton(text='Place an order ✅', callback_data='order')
    cart = InlineKeyboardButton(text='Cart 🗑', callback_data='cart')
    # phone_button = InlineKeyboardButton(text='📩 Написать администратору', callback_data='phone_button')

    # Генерация кнопок с товарами ( базы данных )
    all_products = [InlineKeyboardButton(text=f'{i[0]}', callback_data=i[1]) for i in get_pr_name_id]
    print(all_products)

    # Обединить наши кнопки с пространством
    buttons.row(order)
    buttons.add(*all_products)
    buttons.row(cart)
    # buttons.row(phone_button)

    return buttons

# Кнопки для выбора кол-во
def choose_product_count(plus_or_minus='', current_amount=1):
    # Создаем пространство для кнопок
    buttons = InlineKeyboardMarkup(row_width=3)

    # Несгораемые кнопки
    back = InlineKeyboardButton(text='Back', callback_data='back')
    plus = InlineKeyboardButton(text='+', callback_data='plus')
    minus = InlineKeyboardButton(text='-', callback_data='minus')
    count = InlineKeyboardButton(text=str(current_amount), callback_data=str(current_amount))
    cart = InlineKeyboardButton(text='Add to cart ➕', callback_data='to_cart')

    #Отслеживать плюс или минус
    if plus_or_minus == 'plus':
        new_amount = int(current_amount) + 1
        print(f'bt.cpc plus{new_amount}')

        count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
        print(f"bt.cpc vixod {count}")

    elif plus_or_minus == 'minus':
        if int(current_amount) > 1:
            new_amount = int(current_amount) - 1
            print(f'bt.cpc minus{new_amount}')

            count = InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
            print(f"bt.cpc vixod {count}")

    # Обединить кнопки с пространством
    buttons.add(minus, count, plus)
    buttons.row(cart)
    buttons.row(back)

    return buttons

# кнопки что бы подтвердить заказ
def get_accept():
    buttons = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Confirm')
    no = KeyboardButton('Cancel')

    buttons.add(yes, no)

    return buttons

# Кнопка для перехода в корзину
def get_cart():
    buttons = InlineKeyboardMarkup(row_width=1)

    clear_cart = InlineKeyboardButton(text='Empty Trash 🗑', callback_data='clear_cart')
    order = InlineKeyboardButton(text='Place an order ✅', callback_data='order')
    back = InlineKeyboardButton(text='Cancel ⬅️', callback_data='back')

    buttons.add(clear_cart, order, back)

    return buttons


def choice_buttons():
    # Создать пространство для кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создаем кнопки
    service_button = types.KeyboardButton('Order a service')

    # Добавляем кнопки в пространство
    buttons.add(service_button)

    # вернем все эти значени
    return buttons


def number_buttons():
    # Создать пространство для кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    num_button = types.KeyboardButton('Share contact 📞', request_contact=True)

    buttons.add(num_button)

    return buttons


def geo_buttons():
    # Создать пространство для кнопок
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)

    g_button = types.KeyboardButton('Share', request_location=True)

    buttons.add(g_button)

    return buttons

# кнопки для подтверждения заказа
def get_accept_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    yes = KeyboardButton('Confirm')
    no = KeyboardButton('Cancel')

    kb.add(yes, no)

    return kb