#coding=utf8
import requests
import lxml
import smtplib
from bs4 import BeautifulSoup as Soup
from firebase import firebase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

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

        fb.post('/'+key, {'title': title, 'url': url})

isad_url = "http://isad.oia.ncku.edu.tw/files/40-1381-11-1.php?Lang=zh-tw"
ird_url = "http://ird.oia.ncku.edu.tw/files/40-1382-11-1.php?Lang=zh-tw"
iisd_url = "http://iisd.oia.ncku.edu.tw/files/40-1383-11-1.php?Lang=zh-tw"

query = ".baseTB.listSD tr.row_1 .h5 a, .baseTB.listSD tr.row_2 .h5 a"

fb_url = "https://ncku-inte-crawler.firebaseio.com/"
secret = "V164livV3QtVxWBJWTQERIAoI9XVSWs64v6kxtcC"
email = "nckuintecrawler@gmail.com"
pwd = "ncku2757575"

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
    news_now = [{'title': news.get_text(),'url': news.get("href") } for news in newses]

    result = fb.get(path, None) 
    if result != None :
        news_old = [result[k] for k in result]
    else:
        news_old = []

    if (sorted(news_now) == sorted(news_old)):
        print(key+": Data up to date.")
    else:
        print(key+": Data update!")

        subject = "國際事務處資訊更新報 - " + dept[key]
        html = dept[key] + ": <br />" 

        for n in news_now:
            html += '<a href="' + n['url'] + '">' + n['title'].encode('utf8') + '</a><br /><br />'

        with open("emails.txt") as f:
            for e in f:
                sendMail(email, pwd, e, subject, html)

        fb.delete(path, None)
        post_all(path, news_now)


