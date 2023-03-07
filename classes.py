class SQLHelper:
    def __init__(self, mainsql, bot):
        self.mainsql = mainsql
        self.bot = bot


    def userstate(self, user_id, newstate):
        self.mainsql.execute("UPDATE userdata "
                        "SET state=? "
                        "WHERE userid=?", (newstate, user_id,))
        self.fmainsql.commit()

    def delete_all_from_userid(self, user_id):
        for i in self.mainsql.execute("SELECT userdata.chatid, messagedelete.messageid FROM "
                                      "userdata INNER JOIN messagedelete ON userdata.userid = messagedelete.userid").fetchall():
            self.bot.delete_message(i[0], i[1])


    def chatstate(self, chat_id, newstate):
        self.mainsql.execute("UPDATE userdata "
                        "SET state=? "
                        "WHERE chatid=?", (newstate, chat_id,))
        self.mainsql.commit()


    def active_filters(self, user_id):
        return self.mainsql.execute("SELECT filtername FROM activefilters WHERE userid=?", (user_id,)).fetchall()


    def exists(self, user_id):
        return len(self.mainsql.execute("SELECT * FROM userdata WHERE userid=?", (user_id,)).fetchall()) > 0