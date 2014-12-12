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

class RegistRedmineFirefox(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
        self.verificationErrors = []
        self.accept_next_alert = True
        utils.login(self.driver)
    
    def test_regist_redmine_firefox(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"設定").click()
        driver.find_element_by_link_text(u"インシデント管理").click()
        driver.find_element_by_id("edit-incident-trackers-button").click()
        driver.find_element_by_id("addIncidentTrackerButton").click()
        driver.find_element_by_id("editIncidentTrackerNickname").clear()
        driver.find_element_by_id("editIncidentTrackerNickname").send_keys("red1")
        driver.find_element_by_id("editIncidentTrackerBaseURL").clear()
        driver.find_element_by_id("editIncidentTrackerBaseURL").send_keys("http://10.0.3.41")
        driver.find_element_by_id("editIncidentTrackerProjectId").clear()
        driver.find_element_by_id("editIncidentTrackerProjectId").send_keys("1")
        driver.find_element_by_id("editIncidentTrackerUserName").clear()
        driver.find_element_by_id("editIncidentTrackerUserName").send_keys("f3e284a58ce064fc0af59407f061ca64729e5279")
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click()
        time.sleep(0.5)
        tr_size = len(driver.find_element_by_id("incidentTrackersEditorMainTable").find_elements_by_tag_name("tr"))
        try: self.assertEqual("red1", driver.find_element_by_xpath("//table[@id='incidentTrackersEditorMainTable']/tbody/tr[" + str(tr_size - 1) + "]/td[4]").text)
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
