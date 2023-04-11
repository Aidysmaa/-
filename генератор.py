import string
import sqlite3
from tkinter import *
from tkinter import ttk
from random import choice



def click_button():
    password = ''
    for x in range(20):
        password += choice(char)
    label["text"] = password



def save():
    new_title = title.get()
    if label["text"] == "Здесь будет сгенерированный пароль":
        error["text"] = "Сгенерируйте пароль"
    elif new_title == '':
        error["text"] = "Введите название для сохранения"
    else:
        cursor.execute("""INSERT INTO passwords(title,password)
                    VALUES(?,?)""", (new_title, label["text"]))
        db.commit()
        cursor.execute("SELECT * FROM passwords WHERE title=(?) AND password=(?) LIMIT 1", (new_title, label["text"]))
        tree.insert("", END, values=cursor.fetchone())
        error["text"] = "Пароль сохранен"



def copy():
    if label["text"] == "Здесь будет сгенерированный пароль":
        error["text"] = "Сгенерируйте пароль"
    else:
        value = label["text"]
        root.clipboard_clear()
        root.clipboard_append(value)



with sqlite3.connect("pswd.db") as db:
    cursor = db.cursor()
cursor.execute(""" CREATE TABLE IF NOT EXISTS passwords(id integer PRIMARY KEY AUTOINCREMENT,
                title text NOT NULL, password text NOT NULL);""")

char = string.ascii_letters + string.digits + "!@#$%^&*()_+=-"
password = "Здесь будет сгенерированный пароль"


root = Tk()
root.title("Генератор паролей")
root.geometry("300x350")


error = Message(text="", width=400)
error.config(padx=0)
label = Label(text=password)
generate_btn = Button(text="Сгенерировать пароль", command=click_button)
title = Entry()
save_btn = Button(text="Сохранить", command=save)
copy_btn = Button(text="Копировать в буффер", command=copy)
columns = ("id", "name", "password")
tree = ttk.Treeview(columns=columns, show="headings", height=10)


generate_btn.pack()
label.pack()
copy_btn.pack()
title.pack()
save_btn.pack()
error.pack()
tree.pack()


tree.heading("id", text="id", anchor=W)
tree.heading("name", text="name", anchor=W)
tree.heading("password", text="password", anchor=W)
tree.column("#1", stretch=NO, width=20)
tree.column("#2", stretch=NO, width=70)
tree.column("#3", stretch=NO, width=200)
cursor.execute("SELECT * FROM passwords")
pswds = cursor.fetchall()
for pswd in pswds:
    tree.insert("", END, values=pswd)

root.mainloop()
