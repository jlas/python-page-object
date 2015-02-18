#!/usr/bin/env python

from selenium import webdriver

from lnkdn_pages import LoginPage, PeoplePage

driver = webdriver.Firefox()

lp = LoginPage(driver)
hp = lp._open().signIn('username', 'password')
cp = PeoplePage(driver)
cp._open()
cp.connect()