This is a web crawler to grab informations from Office of International Affairs of NCKU, and it can automatically send a email notification by gmail if there is something update on the website.

# Requirement

You need a [Firebase](https://firebase.google.com/) application to store the data.

You also need a gmail account as mail sending server.

Python Packages
```
requests
beautifulsoup4
lxml
python-firebase
firebase-token-generator
```

# Installation

```
$ git clone https://github.com/team6612/ncku-inte-crawler.git
$ cd ncku-inte-crawler
$ sudo pip install -r requirements.txt
```

Configure the configuration file.

```
$ cp config.example config
$ nano config
```

After config you can run `python crawler.py`. If setting is correct, it'll crawl all information from iisd, ird and isad's first news page and send an email to destination mails.

You may need task scheduling to check out the status of websites. I use `crontab` on my ubuntu server.

# LIcense
This project is licensed under the terms of the MIT license.
