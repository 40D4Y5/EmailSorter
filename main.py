try:
    import os
    import time
    import sys
    import re
    import sqlite3
    from sqlite3 import Error
    from colorama import Fore as F
except ImportError as error:
    print(f"{error.__class__.__name__}: {error} - Please Install Modules using pip install <name>")
try:
    from includes.extra import banner, green_box, blue_box, info_box, red_box
except ImportError:
    print("Please Include the folder includes and the extra.py !!!")


class email_sorter:
    def __init__(self):
        self.email = []
        self.aol = 0
        self.domain = 0
        self.gmail = 0
        self.homtmail = 0
        self.icloud = 0
        self.proton = 0
        self.yahoo = 0
        self.yandex = 0
        self.usa = 0

    def main(self):
        global con
        banner()
        fileN = input(info_box + " Enter name with file extention format: ")
        start_time = time.time()
        filename1 = self.readFile(fileN)
        self.sqle_creat()
        self.email = self.Loademails(filename1)
        self.data_store(self.email)
        self.sortEmails()
        total = self.aol + self.domain + self.gmail + self.homtmail + self.icloud \
            + self.proton + self.yahoo + self.yandex
        print(red_box + "Total emails = "+str(total)+"\n" + blue_box + " Aol Emails = " + str(self.aol) + " Gmail = "+str(self.gmail) + " Hotmail = "+str(self.homtmail) +
              " Icloud emails = " + str(self.icloud) + " Yhoo = "+str(self.yahoo) + " Yandex = "+str(self.yandex) + " Protonmail = " + str(self.proton) + " Random Email = "+str(self.domain))
        print(info_box+" Sorted in" + "--- %s seconds ---" %
              (time.time() - start_time))
        con.close()

    def sqle_creat(self):
        global con
        try:
            con = sqlite3.connect('leads.db')
            cursor = con.cursor()
            cursor.execute(
                "create table if not exists Emails(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, email TEXT NOT NULL UNIQUE )")
            con.commit()
        except Error:
            print(Error)

    def data_store(self, email):
        global con
        cursor = con.cursor()
        for i in email:
            try:
                cursor.execute("INSERT INTO Emails(email) VALUES (?)", (i))
                con.commit()
                print(F.GREEN + f"Added to Database ---------> {i}")
            except sqlite3.IntegrityError:
                print(F.RED+f"Already in Database -------> {i}")

    def readFile(self, filename):

        filename = filename
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filDir = os.path.join(fileDir, filename)

        if os.path.isfile(filDir):
            return(filDir)

        else:
            print(red_box+" Please check the file name again")
            newf = input(info_box+" Eneter file name again :")
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            filDir = os.path.join(fileDir, newf)

            if os.path.isfile(filDir):
                return(filDir)

            else:
                self.readFile(filename)

    def Loademails(self, filename):
        file = open(filename, 'r', encoding='utf8')
        email = []
        try:
            for line in file.readlines():
                s = re.findall(
                    r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', line)
                if len(s) > 1:
                    for i in s:
                        email.append([i])
                else:
                    email.append(s)
        except Exception as e:
            print(red_box+f"Error reading and Finding the file {e}")
        return email

    def sortEmails(self):
        global con
        mypath = 'results'

        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        cursor = con.cursor()
        cursor.execute("SELECT email FROM Emails")
        rows = cursor.fetchall()
        email = [row for row in rows]
        # print(email)

        for h in email:
            emailstr = ''
            emailstr = ''.join(h)
            na = emailstr.split('@')[-1]
            name = na.split('.')[0]+".txt"
            with open(f'results/{name}', 'a') as f:
                f.write(emailstr+'\n')


if __name__ == "__main__":
    email = email_sorter()
    email.main()
