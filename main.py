try:
    import os
    import time
    import sys
    import re
    import sqlite3
    import csv
    import concurrent.futures
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
        self.choice = 0
        self.email = []
        self.email_domains = {}
        self.domains = []
        banner()

    def main(self):
        global con

        self.menue()
        if self.choice == '0':
            fileN = input(
                info_box + f" Enter name with file extention format: {green_box}")
            start_time = time.time()
            filename1 = self.readFile(fileN)
            self.email = self.Loademails(filename1)
            self.sortEmails(self.email)
            print(
                f'{green_box} {self.email_domains} Uuique Domains: {len(self.email_domains)}')
            print('\n')
            print(info_box+" Sorted in" + "--- %s seconds ---" %
                  (time.time() - start_time))
            print('\n')
            con.close()
            self.main()

        elif self.choice == '1':
            fileN = input(
                info_box + f" Enter name with file extention format: {green_box}")
            start_time = time.time()
            filename1 = self.readFile(fileN)
            self.email = self.Loademails(filename1)
            self.sqle_creat()
            with concurrent.futures.ThreadPoolExecutor()as executor:
                executor.map(self.data_store, self.email)
            print(
                f'{green_box} {self.email_domains} Uuique Domains: {len(self.email_domains)}')
            print('\n')
            print(info_box+" Added to Database in in" +
                  "--- %s seconds ---" % (time.time() - start_time))
            print('\n')
            self.main()

        elif self.choice == '2':
            start_time = time.time()
            self.sqle_creat()
            e = self.Extract_emails_db()
            self.sortEmails(e)
            print(
                f'{green_box} {self.email_domains} Uuique Domains: {len(self.email_domains)}')
            print('\n')
            print(info_box+" Sorted in" + "--- %s seconds ---" %
                  (time.time() - start_time))
            print('\n')
            con.close()
            self.main()

        elif self.choice == '3':
            start_time = time.time()
            e = self.query_select()
            self.sortEmails(e)
            print(
                f'{green_box} {self.email_domains} Uuique Domains: {len(self.email_domains)}')
            print(info_box+" Sorted in" + "--- %s seconds ---" %
                  (time.time() - start_time))
            print('\n')
            con.close()
            self.main()

        elif self.choice == '6':
            exit()

        else:
            self.main()

        # fileN = input(info_box + " Enter name with file extention format: ")
        # start_time = time.time()
        # filename1 = self.readFile(fileN)
        # self.sqle_creat()
        # self.email = self.Loademails(filename1)
        # with concurrent.futures.ThreadPoolExecutor()as executor:
        #     results = executor.map(self.data_store, self.email)
        # # self.data_store(self.email)
        # self.sortEmails()
        # total = self.aol + self.domain + self.gmail + self.homtmail + self.icloud \
        #     + self.proton + self.yahoo + self.yandex
        # print(red_box + "Total emails = "+str(total)+"\n" + blue_box + " Aol Emails = " + str(self.aol) + " Gmail = "+str(self.gmail) + " Hotmail = "+str(self.homtmail) +
        #       " Icloud emails = " + str(self.icloud) + " Yhoo = "+str(self.yahoo) + " Yandex = "+str(self.yandex) + " Protonmail = " + str(self.proton) + " Random Email = "+str(self.domain))
        # print(info_box+" Sorted in" + "--- %s seconds ---" %
        #       (time.time() - start_time))
        # con.close()

    def menue(self):
        print(f'\t{info_box} -------Menue-------')
        print(f'{info_box} 0 ------- Sort emails Without adding them to database')
        print(f'{info_box} 1 ------- Add Emails to Database')
        print(f'{info_box} 2 ------- Extract all Emails from database')
        print(f'{info_box} 3 ------- Extract specific Emails from database')
        print(f'{info_box} 4 ------- Delete Emails from Database')
        print(f'{info_box} 5 ------- Email Checker from file')

        print(f'{info_box} 6 ------- Exit')
        self.choice = input(
            f'{blue_box} Enter your Choice number: {green_box} ')

    def query_select(self):
        global con
        try:

            query = input(
                f"{blue_box} Enter Email Domain to extract ex. yahoo: ")
            con = sqlite3.connect('leads.db')
            cursor = con.cursor()
            cursor.execute(
                "SELECT email FROM Emails WHERE email LIKE \"%@" + query + "%\"")
            rows = cursor.fetchall()
            email = [row for row in rows]
            if len(email) == 0:
                print(f"{red_box} empty query")
            return email
        except Exception as e:
            print(e)

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
        con1 = sqlite3.connect('leads.db')
        cursor = con1.cursor()
        try:
            cursor.execute("INSERT INTO Emails(email) VALUES (?)", (email))
            con1.commit()
            con1.close()
            print(F.GREEN + f"Added to Database ---------> {email}")
            emailstr = ''
            emailstr = ''.join(email)
            na = emailstr.split('@')[-1]
            if na.split('.')[0] not in self.domains:
                self.email_domains[na.split('.')[0]] = 1
                self.domains.append(na.split('.')[0])
            else:
                self.email_domains[na.split('.')[0]] += 1
        except sqlite3.IntegrityError:
            con1.close()
            print(F.RED+f"Already in Database -------> {email}")

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
        email = []
        if filename.endswith('.txt'):
            file = open(filename, 'r', encoding='utf8')

            try:
                for line in file.readlines():
                    s = re.findall(
                        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', line)
                    if s == []:
                        continue
                    elif len(s) > 1:
                        for i in s:
                            email.append([i])
                    else:
                        email.append(s)
            except Exception as e:
                print(red_box+f"Error reading and Finding the file {e}")

        elif filename.endswith('.csv'):
            email = []
            with open(filename, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                for line in csv_reader:
                    if len(line) > 1:
                        for i in line:
                            s = re.findall(
                                r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', i)
                            if s == []:
                                continue
                            elif len(s) > 1:
                                for i in s:
                                    email.append([i])
                            else:
                                email.append(s)

                    else:
                        s = re.findall(
                            r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', line)
                        if s == []:
                            continue
                        elif len(s) > 1:
                            for i in s:
                                email.append([i])
                        else:
                            email.append(s)
        clean = []
        for i in email:
            if i not in clean:
                clean.append(i)
        return clean

    def Extract_emails_db(self):
        global con
        cursor = con.cursor()
        cursor.execute("SELECT email FROM Emails")
        rows = cursor.fetchall()
        email = [row for row in rows]
        return email

    def sortEmails(self, email):
        mypath = 'results'

        if not os.path.isdir(mypath):
            os.makedirs(mypath)
        # cursor = con.cursor()
        # cursor.execute("SELECT email FROM Emails")
        # rows = cursor.fetchall()
        # email = [row for row in rows]
        # print(email)

        for h in email:
            emailstr = ''
            emailstr = ''.join(h)
            na = emailstr.split('@')[-1]
            if na.split('.')[0] not in self.domains:
                self.email_domains[na.split('.')[0]] = 1
                self.domains.append(na.split('.')[0])
            else:
                self.email_domains[na.split('.')[0]] += 1
            name = na.split('.')[0]+".txt"
            with open(f'results/{name}', 'a') as f:
                f.write(emailstr+'\n')


if __name__ == "__main__":
    email = email_sorter()
    email.main()
