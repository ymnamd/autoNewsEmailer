from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os
import sys
import smtplib
from email.message import EmailMessage


# WEB SCRAPING SECTION
app_path = os.path.dirname(sys.executable)

now = datetime.now()
date = now.strftime("%d-%m-%Y")

website = "https://www.abc.net.au/news"
path = "/Users/yameenahmed/PycharmProjects/automation/chromedriver-mac-arm64/chromedriver"

options = Options()
options.add_argument("--headless=new")

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)

# containers = driver.find_elements(by="xpath", value='//div[@class="col sun-col-2"]')
containers = driver.find_elements(by="xpath", value='//li[@data-component="ListItem"]')
# //div[@class="teaser__copy-container"]/a/h3


titles = []
subtitles = []
links = []

n = 10
for container in containers:
    if n>0:
        title = container.find_element(by='xpath', value='./div/div/div').text
        subtitle = container.find_element(by='xpath', value='./div/div/div[@class="Typography_base__sj2RP VolumeCard_synopsis__IWGFK VolumeCard_hideForMobile__HHKc5 Typography_sizeMobile14__u7TGe Typography_lineHeightMobile24__crkfh Typography_regular__WeIG6 Typography_colourInherit__dfnUx"]').text
        link = container.find_element(by='xpath', value='./div/div/div/a').get_attribute('href')
        titles.append(title)
        subtitles.append(subtitle)
        links.append(link)
        n-=1
    else:
        break

# my_dict = {'title': titles, 'subtitle': subtitles, 'link': links}

# df_headlines = pd.DataFrame(my_dict)
# file_name = f"headline-{date}.csv"
# final_path = os.path.join(app_path, file_name)
# df_headlines.to_csv(final_path)

driver.quit()


# EMAIL SECTION
body = ""
for i in range(len(titles)):
    body+=(f"Title: {titles[i]}\n")
    body+=(f"Description: {subtitles[i]}\n")
    body+=(f"Link: {links[i]}\n\n")

msg = EmailMessage()
msg.set_content(body)
msg['subject'] = f"Today's News from ABC News {date}"
msg['to'] = "yameen.aus@gmail.com"

user = "automationemail285@gmail.com"
msg['from'] = user
pw = "rcqk pywq udwn azva"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, pw)
server.send_message(msg)
server.quit()