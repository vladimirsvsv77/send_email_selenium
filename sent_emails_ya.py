# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from time import sleep
import json


user_data = json.loads(open('leap_json.json').read())
YOUR_EMAIL = ""
YOUR_PASS = ""

class SentEmail(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.subject = "Friendly request from Leap"
        self.text_mess = """
Hi {NAME}, 

My name is Lisa. I'm a marketing specialist, and currently I'm working on a research named "Startups are hiring". I found your email on Leap. 

I was wondering if you could help me and take part in my research? I have a few questions about the experience with hiring people. It shouldn't take longer than 10 minutes. Your help will be much appreciated. 

Look forward to hearing from you.

Kind regards, 
Lisa
""".encode('utf-8')
    
    def test_sent_email(self):
        driver = self.driver
        self.auth()
        
        sleep(1)

        count = 0
        for i in user_data:
            print(i['u_data']['email'])
            print(count)
            try:
                self.sent_email(i['u_data']['email'], 
                            self.subject, 
                            self.text_mess.replace("{NAME}", i['u_data']['full_name'].encode('utf-8').split(" ")[0]))
                count += 1
            except:
                continue

    def auth(self):
        driver = self.driver
        driver.get("https://passport.yandex.ru/auth?mode=add-user&retpath=https%3A%2F%2Fyandex.ru%2F")
        driver.find_element_by_id("passp-field-login").clear()
        driver.find_element_by_id("passp-field-login").send_keys(YOUR_EMAIL)
        driver.find_element_by_id("passp-field-login").click()
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Зарегистрировать'])[1]/following::button[1]").click()
        driver.find_element_by_id("passp-field-passwd").clear()
        driver.find_element_by_id("passp-field-passwd").send_keys(YOUR_PASS)
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Не помню пароль'])[1]/following::button[1]").click()
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Почта'])[1]/following::div[1]").click()


    def sent_email(self, email, subject, text):
        driver = self.driver
        sleep(2)
        driver.find_element_by_link_text(u"Написать").click()
        sleep(2)
        driver.find_element_by_name("subj-99fee024ceee654c736577741439e28b713ea72d").send_keys(subject)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Кому'])[1]/following::div[2]").send_keys(email)
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Без оформления'])[1]/following::div[3]").send_keys(text)
        sleep(2)
        driver.find_element_by_xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Снять выделение'])[1]/following::span[6]").click()
        sleep(2)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
