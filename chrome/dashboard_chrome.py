# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import sys
sys.path.append('../')
import utils

class Dashboard(unittest.TestCase):
    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        utils.login(self.driver)
    
    def test_dashboard(self):
        time.sleep(1)
        driver = self.driver
        driver.get(self.base_url + "/ajax_dashboard")
        try: self.assertEqual(u"ダッシュボード - Hatohol", driver.title)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"ダッシュボード", driver.find_element_by_css_selector("h2").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"グローバルステータス", driver.find_element_by_xpath("//div[@id='main']/div[2]/div/b").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"システムステータス", driver.find_element_by_xpath("//div[@id='main']/div[3]/div/b").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"ホストステータス", driver.find_element_by_xpath("//div[@id='main']/div[4]/div/b").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Copyright © 2013-2014 Project Hatohol", driver.find_element_by_xpath("//div[5]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
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
