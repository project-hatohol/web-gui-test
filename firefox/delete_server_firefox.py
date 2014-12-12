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

class FRegistNagios(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        utils.login(self.driver)
    
    def test_f_regist_nagios(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"設定").click()
        driver.find_element_by_link_text(u"監視サーバー").click()
        before_host_name = driver.find_element_by_xpath("//table[@id='table']/tbody/tr[1]/td[4]").text
        driver.find_element_by_xpath("(//input[@type='checkbox'])[1]").click()
        driver.find_element_by_id("delete-server-button").click()
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        time.sleep(1)
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button[type=\"button\"]").click()
        tr_size = len(driver.find_element_by_id("table").find_elements_by_tag_name("tr"))
        try: self.assertNotEqual(before_host_name, driver.find_element_by_xpath("//table[@id='table']/tbody/tr[1]/td[4]").text)
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
