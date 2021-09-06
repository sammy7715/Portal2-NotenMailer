import requests
from bs4 import BeautifulSoup
import time
import smtplib
import datetime

#Email data
sender_mail = "EXAMPLE@gmail.com" # @gmail adress required
sender_password = "EMAILPASSWORD"
receiver = "MUSTER@XYZ.de" # Empfänger Mailadresse
message = 'Subject: {}\n\n{}'.format("Neue Noten", "Portal2 Checken!")

sleeptime = 7200 #Zeit zwischen Seitenaufrufen in Sekunden, standardmässig auf 2 Stunden
login_data = {
    'username': 'PORTAL2LOGINNAME',
    'password': 'PORTAL2PASSWORD',
    'execution': 'e1s1',
    '_eventId': 'submit',
    'sumbit': 'Anmelden'
}

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Connection':'keep-alive'
}

def getData():
    s = requests.Session()
    urlPortal2 = 'https://cas.uni-mannheim.de/cas/login?service=https%3A%2F%2Fportal2.uni-mannheim.de/portal2/rds%3Fstate%3Duser%26type%3D1'
    url1 = 'https://portal2.uni-mannheim.de/portal2/pages/cs/sys/portal/hisinoneStartPage.faces?chco=y'
    urlPruefungsverwaltung = 'https://portal2.uni-mannheim.de/portal2/rds?state=change&type=1&moduleParameter=studyPOSMenu&nextdir=change&next=menu.vm&subdir=applications&xml=menu&purge=y&navigationPosition=hisinoneMeinStudium%2CstudyPOSMenu&recordRequest=true&breadcrumb=studyPOSMenu&subitem=studyPOSMenu&topitem=hisinoneMeinStudium'
    
    r = s.get(urlPortal2, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    login_data['lt']=soup.find('div',{'class':'button-group'}).input.get('value')
    r = s.post(urlPortal2, data=login_data, headers=headers)
    r = s.get(url1, headers=headers)
    r = s.get(urlPruefungsverwaltung, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    url3 = soup.find('div',{'class':'divcontent'}).div.div.form.div.ul.findAll('li')[2].a.get('href')
    r = s.get(url3, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    planUrl = soup.find('div',{'class':'divcontent'}).div.form.ul.li.findAll('a')[1].get('href')
    r = s.get(planUrl, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('div',{'class':'divcontent'}).div.form.findAll('table')[1]
    s.close()
    return table

def monitor():
        old = getData()
        while True:
            now = datetime.datetime.now()
            if now.hour >= 8 and now.hour <= 22:
                new = getData()
                if old != new:
                    server =  smtplib.SMTP_SSL('smtp.gmail.com',465)
                    server.login(sender_mail,sender_password)
                    print("Email login worked")
                    server.sendmail(sender_mail,receiver,message)
                    print("mail sent")
                    server.quit()
                    old = new
                    print("Änderung!")
                else:
                    print("keine Änderung!")
            time.sleep(sleeptime)

monitor()
