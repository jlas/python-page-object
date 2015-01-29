#!/usr/bin/env python

from selenium import webdriver

from okc_pages import LoginPage

lp = LoginPage(webdriver.Firefox())
hp = lp._open().signIn('username', 'password')
mp = hp.clickBrowseMatches()
mp.visitAllMatches(matchLimit=1000)
