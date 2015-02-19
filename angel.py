#!/usr/bin/env python

from selenium import webdriver

from angel_pages import LoginPage, RecruitingPage

driver = webdriver.Firefox()

lp = LoginPage(driver)
jp = lp._open().signIn('username', 'password')

# e.g. rp = RecruitingPage(driver, roles=['Sales'], locations=['New York City'], keywords=['Python'])
rp = RecruitingPage(driver, roles=['Sales'])

rp._open()
rp.connect()