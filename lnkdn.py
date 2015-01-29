#!/usr/bin/env python

from selenium import webdriver

from lnkdn_pages import LoginPage

lp = LoginPage(webdriver.Firefox())
hp = lp._open().signIn('username', 'password')
