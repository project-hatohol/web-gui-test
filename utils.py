# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

def login(driver):
    driver.get("http://127.0.0.1:8000")
    driver.find_element_by_id("inputUserName").clear()
    driver.find_element_by_id("inputUserName").send_keys("admin")
    driver.find_element_by_id("inputPassword").clear()
    driver.find_element_by_id("inputPassword").send_keys("hatohol")
    driver.find_element_by_id("loginFormSubmit").click()
