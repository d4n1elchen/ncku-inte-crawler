#coding=utf8
import requests
import lxml
import smtplib
import os
import ConfigParser                    
from bs4 import BeautifulSoup as Soup
from firebase import firebase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from operator import itemgetter

def sendMail(strGmailUser,strGmailPassword,strRecipient,strSubject,strContent):
    strMessage = MIMEMultipart()
    strMessage['From'] = strGmailUser
    strMessage['To'] = strRecipient
    strMessage['Subject'] = strSubject
    strMessage.attach(MIMEText(strContent, 'html'))
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(strGmailUser, strGmailPassword)
    mailServer.sendmail(strGmailUser, strRecipient, strMessage.as_string())
    mailServer.close()
    return 'send successed'

def post_all(path, datas):
    
    for d in datas:

        title = d['title']
        url = d['url']
        date = d['date']

        fb.post('/'+key, {'title': title, 'url': url, 'date': date})

config = ConfigParser.RawConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__))+"/config") 

isad_url = "http://isad.oia.ncku.edu.tw/files/40-1381-11-1.php?Lang=zh-tw"
ird_url = "http://ird.oia.ncku.edu.tw/files/40-1382-11-1.php?Lang=zh-tw"
iisd_url = "http://iisd.oia.ncku.edu.tw/files/40-1383-11-1.php?Lang=zh-tw"

query = ".baseTB.listSD tr.row_1 .h5, .baseTB.listSD tr.row_2 .h5"

fb_url = config.get("Firebase", "url")
secret = config.get("Firebase", "secret")
email = config.get("Firebase", "email") 

gmail = config.get("Gmail", "gmail")
pwd = config.get("Gmail", "pwd") 

mails = config.get("Mails", "mails").replace('\n','').split(',')

urls = { 'isad': isad_url, 'ird': ird_url, 'iisd': iisd_url }
dept = { 'isad': '國際學生事務組', 'ird': '國際合作組', 'iisd': '國際化資訊與服務組' }

auth = firebase.FirebaseAuthentication(secret, email)
fb = firebase.FirebaseApplication(fb_url, auth)

for key, url in urls.viewitems():

    path = '/'+key

    res = requests.get(url)
    res.encoding = 'utf8'
    soup = Soup(res.text, 'lxml')

    s = soup.select

    newses = s(query)
    news_now = [{'title': news.select("a")[0].get_text(),'url': news.select("a")[0].get("href"), 'date': news.select("span")[0].get_text() } for news in newses]

    try:
        result = fb.get(path, None) 
    except:
        type, message, traceback = sys.exc_info()
        while traceback:
            print('..........')
            print(type)
            print(message)
            print('function or module？', traceback.tb_frame.f_code.co_name)
            print('file？', traceback.tb_frame.f_code.co_filename)
            traceback = traceback.tb_next
        continue

    if result != None:
        news_old = [result[k] for k in result]
    else:
        news_old = [{'date': '', 'url': '', 'title': ''}]

    news_now = sorted(news_now, key=itemgetter('date','url'), reverse=True)
    news_old = sorted(news_old, key=itemgetter('date','url'), reverse=True)

    if news_now[0] != news_old[0]:
        print(key+": Data update!")

        old_url =  news_old[0]['url']
        s = next((i for i, n in enumerate(news_now) if n['url'] == old_url), None)

        subject = "國際事務處資訊更新報 - " + dept[key]
        html = dept[key] + ": <br /><br />" 

        for n in news_now[:s]:
            html += '<a href="' + n['url'] + '">' + (n['date'] + n['title']).encode('utf8') + '</a><br /><br />'

        for mail in mails:
            sendMail(gmail, pwd, mail, subject, html)

        fb.delete(path, None)
        post_all(path, news_now)


