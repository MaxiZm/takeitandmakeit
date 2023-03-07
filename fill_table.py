import pandas as pd
import sqlite3 as sq

sqldatabase = sq.connect("botdata.sqlite")

sqldatabase.execute("CREATE TABLE IF NOT EXISTS gadgets (id int, brand varchar(50), model varchar(50), RAM inr, MEM int, processor varchar(50), color varchar(50), country varchar(50))")

print(list(sqldatabase.execute("SELECT * FROM gadgets")))

data = pd.read_excel("Gadgets.xlsx")
sqldata = ['brand', 'model', 'RAM', 'MEM', 'processor', 'color', 'country']

for i in data.iloc:
    if len(list(sqldatabase.execute(f"SELECT * FROM gadgets WHERE id == {i[2]}"))) == 0:
        data_to_add = []
        for info in sqldata:
            data_to_add.append(input(f'{i}, {info}:\t').strip())

        data_to_add = list(map(lambda x: x if x.isdigit() or x.lower() == "null" else "\'"+x+"\'", data_to_add))
        print(f"INSERT INTO gadgets VALUES ({i[2]}, {', '.join(data_to_add)})")
        sqldatabase.execute(f"INSERT INTO gadgets VALUES ({i[2]}, {', '.join(data_to_add)})")
        sqldatabase.commit()
    print(list(sqldatabase.execute("SELECT * FROM gadgets")))
