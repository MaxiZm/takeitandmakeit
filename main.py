import telebot
import telebot.types as types
import classes
import sqlite3

bot = telebot.TeleBot(token="6125750542:AAFhoEar8PQSP6N1-LjdRKPor_vy6_KN73Y")
mainsql = sqlite3.connect("botdata.sqlite", check_same_thread=False)

mainsql.execute("CREATE TABLE IF NOT EXISTS "
                "userdata (userid int PRIMARY KEY, chatid int CHECK ( chatid = NULL OR chatid >= 0), "
                "username varchar(256), state mediumtext(4096))")
mainsql.execute("CREATE TABLE IF NOT EXISTS "
                "activefilters (userid int, filtername varchar(100), FOREIGN KEY (userid) REFERENCES userdata(userid))")
mainsql.execute("CREATE TABLE IF NOT EXISTS cart (userid int, productid int, "
                "FOREIGN KEY (userid) REFERENCES userdata(userid), FOREIGN KEY (productid) REFERENCES gadgets(id))")
mainsql.execute("CREATE TABLE IF NOT EXISTS messagedelete (userid int, messageid int, "
                "FOREIGN KEY (userid) REFERENCES userdata(userid))")

def main_menu():
    menuKb = types.ReplyKeyboardMarkup()
    ordersBtn = types.KeyboardButton(text="Мои Заказы🚀")
    cartBtn = types.KeyboardButton(text="Корзина🛒")
    katalogBtn = types.KeyboardButton(text="Каталог📱")
    menuKb.add(ordersBtn, cartBtn, katalogBtn)
    return menuKb


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать в магазин по продаже телефонов! Мы предлагаем выгодные "
                                      "условия для приобретения телефонов оптом. У нас вы можете найти недорогие и "
                                      "качественные телефоны, которые подойдут для любого бюджета. Покупайте у нас и "
                                      "получайте наилучшие условия!", reply_markup=main_menu())
    if exists(message.from_user.id):
        chatstate(message.chat.id, "")
    else:
        mainsql.execute("INSERT INTO userdata VALUES "
                        "(?, ?, ?, ?)", (message.from_user.id, message.chat.id, message.from_user.username, ""))
        mainsql.commit()


@bot.message_handler(content_types=["text"])
def main_thread(message):
    if not exists(message.from_user.id):
        start(message)

    if message.text == "Каталог📱":
        chatstate(message.chat.id, "catalog")

        catalogchoice = types.InlineKeyboardMarkup()
        filterchosen = types.InlineKeyboardButton("Фильтр🔻", callback_data="catalogfilter")
        searchnamechosen = types.InlineKeyboardButton("По тексту🔎", callback_data="catalogtext")
        allchosen = types.InlineKeyboardButton("Всё☮️", callback_data="catalogall")
        catalogchoice.add(filterchosen, searchnamechosen, allchosen)

        bot.send_message(message.chat.id, "Выберите тип поиска по каталогу:", reply_markup=catalogchoice)


@bot.callback_query_handler(lambda query: query.data == "catalogall")
def catalogall(query):
    q = mainsql.execute("SELECT brand, model, RAM, MEM, processor, color, country FROM gadgets").fetchall()
    txt = map(lambda x: f"*{x[0]} {x[1]}* _{x[4]}/{x[2]}Gb/{x[3]}Gb_ {x[5]} {x[6]}", q)
    txt = "\n".join(list(txt))
    bot.send_message(query.message.chat.id, txt, parse_mode="Markdown")
    start(query.message)


bot.infinity_polling()
