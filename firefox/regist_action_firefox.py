# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/../')
import utils

class RegistActionFirefox(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        utils.login(self.driver)
    
    def test_regist_action_firefox(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"設定").click()
        driver.find_element_by_link_text(u"アクション").click()
        driver.find_element_by_id("add-action-button").click()
        Select(driver.find_element_by_id("selectServerId")).select_by_visible_text(u"== 選択 ==")
        driver.find_element_by_xpath("//table[@id='selectorMainTable']/tbody/tr[1]/td[1]").click()
        server_name = driver.find_element_by_xpath("//table[@id='selectorMainTable']/tbody/tr[1]/td[3]").text
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        Select(driver.find_element_by_id("selectHostId")).select_by_visible_text(u"== 選択 ==")
        driver.find_element_by_xpath("//table[@id='selectorMainTable']/tbody/tr[1]/td[1]").click()
        host_name = driver.find_element_by_xpath("//table[@id='selectorMainTable']/tbody/tr[1]/td[3]").text
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        driver.find_element_by_id("inputActionCommand").clear()
        driver.find_element_by_id("inputActionCommand").send_keys("getlog")
        driver.find_element_by_id("inputActionCommand").click()
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button[type=\"button\"]").click()
        time.sleep(0.5)
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button[type=\"button\"]").click()
        time.sleep(0.5)    
        tr_size = len(driver.find_element_by_id("table").find_elements_by_tag_name("tr"))
        try: self.assertEqual(server_name, driver.find_element_by_xpath("//table[@id='table']/tbody/tr[" + str(tr_size - 1) + "]/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(host_name, driver.find_element_by_xpath("//table[@id='table']/tbody/tr[" + str(tr_size - 1) + "]/td[4]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("getlog", driver.find_element_by_xpath("//table[@id='table']/tbody/tr[" + str(tr_size - 1) + "]/td[11]").text)
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
