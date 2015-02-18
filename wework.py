#!/usr/bin/env python

from selenium import webdriver

from wework_pages import LoginPage, DirectoryPage

driver = webdriver.Firefox()

lp = LoginPage(driver)
hp = lp._open().signIn('username', 'password')
dp = DirectoryPage(driver)
dp._open()
dp.connect()