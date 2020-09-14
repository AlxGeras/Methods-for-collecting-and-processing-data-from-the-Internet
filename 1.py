from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
from pprint import pprint



driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://mail.ru')

field_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'mailbox:login-input')))
field_login.send_keys('study.ai_172@mail.ru')
field_login.send_keys(Keys.ENTER)
time.sleep(3)
field_passwd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'mailbox:password-input')))
field_passwd.send_keys('NextPassword172')
field_passwd.send_keys(Keys.ENTER)


first_messege = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, 'llc')
    )
)
first_messege.click()
log = 0

messeges = []
while True:

    messege = {}

    messege_from = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact'))).get_attribute("title")

    messege['from'] = messege_from

    messege_date = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__date'))).text

    messege['date'] = messege_date

    messege_title = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject'))).text

    messege['title'] = messege_title

    messege_text = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter__body'))).text

    messege['text'] = messege_text

    button_next = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'portal-menu-element_next')))


    if len(messeges) == 0:
        messeges.append(messege)
    elif (messeges[len(messeges)-1]['from'] == messege['from'])&\
            (messeges[len(messeges)-1]['date'] == messege['date'])&\
            (messeges[len(messeges)-1]['title'] == messege['title']):
        pass
    else:
         messeges.append(messege)

    button_next.click()
    time.sleep(1)

    if log == 1:
        break

    try:
        driver.find_element_by_xpath("//div[contains(@class,'portal-menu-element_next')]/span[contains(@class,'button2_disabled')]")
        log = 1
    except:
        log = 0


pprint(messeges)



