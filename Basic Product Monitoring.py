# Imports

import time
import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Global Variables (THESE FOUR MUST BE INPUT BY THE USER BETWEEN THE SINGLE QUOTES); email address must be gmail, password is not sent anywhere dangerous only to gmail servers, link is where the product site is; soldout indicator is the html of the page associated with the sold out button.

email = ''
password = ''
link = ''
soldout_indicator = ''

# Extra automatic Global Variable Definitions

soldout_indicator = soldout_indicator.replace(" ", "").replace("\n", "")
to = email
sent_from = email
default_subject = 'Your Product is Probably in Stock!'
default_body = '<html><p>Click <a href = "'+link+'">here</a> to check the status of your product! You will be emailed again in 10 minutes if the product is still available.</p> <p>If you keep receiving emails and the product that you want is not available, respond to this email address, and I will check on the situation as quickly as possible.</p></html>'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# Function Definitions

def alert_email(subj = default_subject, body = default_body, send_to = to):
    '''Sends an email to the address specified by user; body and subject can be changed, but defaults are set above'''
    msg = MIMEText(body, 'html')
    msg['Subject'] = subj
    msg['From'] = sent_from
    msg['To'] = to
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(sent_from,password)
    server.sendmail(sent_from, send_to, msg.as_string())
    server.close()

alert_email(subj = "Your product monitoring has started!", body = "Hope you beat those scalpers.")

# Flow Control With While Loop

while True:
    try:
        product_html = requests.get(link,headers = header).text
        product_html = str(BeautifulSoup(product_html, "html.parser")).replace(" ","").replace("\n","")
        if soldout_indicator in product_html:
            print("The soldout indicator appeared on the page; trying again in 60 seconds")
            time.sleep(60)
            continue
        elif soldout_indicator not in product_html:
            print("The soldout indicator did not appear on the page!")
            alert_email()
            time.sleep(600)
            continue
    except:
        try:
            print("Some type of error has occurred; trying to notify \n\n")
            alert_email("Error occured in order for "+to, "Internet connection down or error expressed; remedy this immediately if possible", "cnferg04@gmail.com")
            time.sleep(30)
        except:
            print("Internet Error encountered and could not notify about it. Trying again soon.")
            time.sleep(300)
        
