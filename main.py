from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os
import sys
import smtplib
from email.message import EmailMessage


# WRB SCRAPING SECTION
app_path = os.path.dirname(sys.executable)

now = datetime.now()
date = now.strftime("%d-%m-%Y")

website = "https://www.thesun.co.uk/sport/football/"
path = "/Users/yameenahmed/PycharmProjects/automation/chromedriver-mac-arm64/chromedriver"

options = Options()
options.add_argument("--headless=new")

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)

containers = driver.find_elements(by="xpath", value='//div[@class="col sun-col-2"]')
# //div[@class="news-tops_group-1"]
# //div[@class="teaser__copy-container"]/a/h3


titles = []
subtitles = []
links = []

for container in containers:
    title = container.find_element(by='xpath', value='./div/div/a/span').text
    subtitle = container.find_element(by='xpath', value='./div/div/a/h3').text
    link = container.find_element(by='xpath', value='./div/div/a').get_attribute('href')
    titles.append(title)
    subtitles.append(subtitle)
    links.append(link)

my_dict = {'title': titles, 'subtitle': subtitles, 'link': links}

df_headlines = pd.DataFrame(my_dict)
# file_name = f"headline-{date}.csv"
# final_path = os.path.join(app_path, file_name)
# df_headlines.to_csv(final_path)

driver.quit()


# EMAIL SECTION
msg = EmailMessage()
msg.set_content(str(my_dict))
msg['subject'] = f"Today's news {date}"
msg['to'] = "yameen.aus@gmail.com"

user = "automationemail285@gmail.com"
msg['from'] = user
pw = "rcqk pywq udwn azva"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, pw)
server.send_message(msg)
server.quit()