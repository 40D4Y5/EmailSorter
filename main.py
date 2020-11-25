try:
    import os
    import time 
    import sys 
    import re 
except ImportError as error:
    print(f"{error.__class__.__name__}: {error} - Please Install Modules using pip install <name>")
try:
    from includes.extra import banner , green_box, blue_box , info_box, red_box
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
    
    def main(self):
        banner()
        fileN = input(info_box +" Enter name with file extention format: ")
        start_time = time.time()
        filename1 = self.readFile(fileN)
        self.fold('Open')
        self.email = self.Loademails(filename1)
        self.sortEmails(self.email)
        self.fold('Close')
        total = self.aol + self.domain + self.gmail + self.homtmail + self.icloud \
            + self.proton + self.yahoo + self.yandex
        print ( red_box +"Total emails = "+str(total)+"\n"+ blue_box +" Aol Emails = "+ str(self.aol) + " Gmail = "+str(self.gmail) + " Hotmail = "+str(self.homtmail) + " Icloud emails = " + str(self.icloud)+ " Yhoo = "+str(self.yahoo) +" Yandex = "+str(self.yandex) +" Protonmail = "+ str(self.proton) + " Random Email = "+str(self.domain))
        print(info_box+"Sorted in" + "--- %s seconds ---" % (time.time() - start_time))

        
    def fold(self, cho):

        global hf , gf , yf, af, xf, pf, mf, rf 
        if cho == 'Open':
            mypath = 'results'
            
            if not os.path.isdir(mypath):
                os.makedirs(mypath)
                hf = open('results/hotmail.txt', 'a+')
                gf = open('results/gmail.txt', 'a+')
                yf = open('results/yahoo.txt', 'a+')
                af = open('results/aol.txt', 'a+')
                xf = open('results/yandex.txt', 'a+')
                pf = open('results/protonmail.txt', 'a+')
                mf = open('results/icouldmail.txt', 'a+')
                rf = open('results/domainmail.txt', 'a+')
            else: 
                hf = open('results/hotmail.txt', 'a+')
                gf = open('results/gmail.txt', 'a+')
                yf = open('results/yahoo.txt', 'a+')
                af = open('results/aol.txt', 'a+')
                xf = open('results/yandex.txt', 'a+')
                pf = open('results/protonmail.txt', 'a+')
                mf = open('results/icouldmail.txt', 'a+')
                rf = open('results/domainmail.txt', 'a+')

        elif cho == 'Close':
            hf.close()
            gf.close()
            yf.close()
            af.close()
            xf.close()
            pf.close()
            mf.close()
            rf.close()
        


        
        
        




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
    def Loademails(self , filename ):
        file = open( filename, 'r', encoding='utf8')
        email = []
        for i in file.readlines():
            try:
                email.append(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', i))
            except Exception:
                continue
        return email


    def sortEmails(self, email):
        global hf , gf , yf, af, xf, pf, mf, rf 
        for h in email:
            emailstr  = ''
            emailstr = ''.join(h)
            if '@hotmail.'  in emailstr or "@live." in emailstr or "@outlook." in emailstr:
                self.homtmail = self.homtmail + 1 
                hf.write(emailstr+'\n')
            elif '@gmail.' in emailstr:
                self.gmail = self.gmail + 1 
                gf.write(emailstr+'\n')
                
            elif 'yahoo.' in emailstr:
                self.yahoo = self.yahoo + 1
                yf.write(emailstr+'\n')
                
            elif '@aol.' in emailstr or '@love.' in emailstr or '@wow.' in emailstr or '@games.' in emailstr or '@ygm.' in emailstr:
                self.aol = self.aol + 1
                af.write(emailstr+'\n')
                
            elif '@yandex.' in emailstr:
                self.yandex = self.yandex + 1
                xf.write(emailstr+'\n')
                
            elif '@protonmail.' in emailstr or '@pm.' in emailstr:
                self.proton = self.proton + 1
                pf.write(emailstr+'\n')
                
            elif '@icloud.' in emailstr or '@me.' in emailstr or '@mac.' in emailstr:
                self.icloud = self.icloud + 1 
                mf.write(emailstr+'\n')
                
            else:
                self.domain = self.domain + 1 
                rf.write(emailstr+'\n')
if __name__ == "__main__":
    email = email_sorter()
    email.main()