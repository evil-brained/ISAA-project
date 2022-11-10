from tkinter import *
import pymongo
import pymysql
from salt_generator import generate_salt
from reg_success import display_success
from reg_failure import display_fail
from password_verifier_generator import function_G
import hashlib
def displayRegistration():
    root = Tk()
    client = pymongo.MongoClient("mongodb://test:test@ac-tfgqiuq-shard-00-00.14ru3v8.mongodb.net:27017,ac-tfgqiuq-shard-00-01.14ru3v8.mongodb.net:27017,ac-tfgqiuq-shard-00-02.14ru3v8.mongodb.net:27017/?ssl=true&replicaSet=atlas-ilkujl-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client['test']
    col=db['users']

    def insert():
        salt = generate_salt()
        username = username_entry.get()
        password = password_entry.get()
        hasher = hashlib.blake2b(digest_size=4)
        hasher.update(str(salt + username + password).encode('utf-8'))
        hash_value = hasher.hexdigest()
        password_verifier = function_G(str(hash_value))
        inp_query = "Insert into user_details(user_name, salt, password_verifier) values (%s, %s, %s);"
        data = (username, salt, password_verifier)
        if username != "" and password != "":
            x=col.insert_one({"username":username,"salt":salt,"password":password_verifier})
            root.destroy()
            display_success()
        else:
            root.destroy()
            display_fail()

    projectName = Label(root, text="ISAA Project")
    projectName.grid(row=0, column=0, pady=5, columnspan=3)
    projectName.config(width=50)
    projectName.config(font=("Arial", 24))

    windowHeading = Label(root, text="Register")
    windowHeading.grid(row=1, column=0, pady=5, columnspan=3)
    windowHeading.config(font=("Arial", 22))

    usernameLabel = Label(root, text="Username*")
    usernameLabel.grid(row=2, column=0, pady=5, columnspan=3)
    usernameLabel.config(font=("Arial", 18))
    username_entry = Entry(root, width=50, borderwidth=5)
    username_entry.grid(row=3, column=0, columnspan=3)

    passwordLabel = Label(root, text="Password*")
    passwordLabel.grid(row=4, column=0, pady=5, columnspan=3)
    passwordLabel.config(font=("Arial", 18))
    password_entry = Entry(root, width=50, borderwidth=5, show="*")
    password_entry.grid(row=5, column=0, columnspan=3)

    registerButton = Button(root, text="REGISTER", command=insert)
    registerButton.grid(row=6, column=0, pady=20, columnspan=3)
    registerButton.config(font=("Arial", 18))

    root.mainloop()
