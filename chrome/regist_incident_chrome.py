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

class RegistIncidentFirefox(unittest.TestCase):
    def setUp(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        utils.login(self.driver)
    
    def test_regist_incident_firefox(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"設定").click()
        driver.find_element_by_link_text(u"インシデント管理").click()
        driver.find_element_by_id("add-incident-setting-button").click()
        server_objects = driver.find_element_by_id("selectIncidentTracker").find_elements_by_tag_name("option")
        server_name = server_objects[0].text
        Select(driver.find_element_by_id("selectIncidentTracker")).select_by_visible_text(server_name)
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button[type=\"button\"]").click()
        time.sleep(0.5)
        driver.find_element_by_css_selector("div.ui-dialog-buttonset > button[type=\"button\"]").click()
        time.sleep(0.5)
        tr_size = len(driver.find_element_by_id("table").find_elements_by_tag_name("tr"))
        name = server_name.split(":", 1)[1].lstrip().encode("utf-8")
        try: self.assertEqual(name, driver.find_element_by_xpath("//table[@id='table']/tbody/tr[" + str(tr_size - 1) + "]/td[7]").text.encode("utf-8"))
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
