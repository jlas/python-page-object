import json
from time import sleep
from random import randint
import urllib

from sel import AbstractBasePage

class LoginPage(AbstractBasePage):

    def __init__(self, webdriver):
        super(LoginPage, self).__init__(webdriver,
            'https://angel.co/login', 'Log In - AngelList')

    def signIn(self, email, password):
        emailEl = self._id('user_email')
        emailEl.send_keys(email)
        passwordEl = self._id('user_password')
        passwordEl.send_keys(password)
        submitEl = self._css('[type="submit"]')
        submitEl.click()
        hp = HomePage(self.webdriver)
        hp._waitUntilOpen()
        return hp

class HomePage(AbstractBasePage):

    def __init__(self, webdriver):
        super(HomePage, self).__init__(webdriver, 'https://angel.co/', 'AngelList')

class JobsPage(AbstractBasePage):

    def __init__(self, webdriver):
        super(JobsPage, self).__init__(webdriver,
            'https://angel.co/jobs', 'Startup Jobs - AngelList')


class RecruitingPage(AbstractBasePage):

    def __init__(self, webdriver, **kwargs):
        '''Open the recruiting page
        @param **kwargs, example of kwargs:
            - roles=['Sales', 'Backend Developer']
            - locations=['New York City']
            - looking_for=['full_time', 'internships', 'contract', 'cofounders']
            - keywords=['Python']
            - colleges=['CMU']
        '''
        baseUrl = ('https://angel.co/candidates#find/f!%s' % json.dumps(kwargs).replace(' ', ''))
        super(RecruitingPage, self).__init__(webdriver, baseUrl, 'Find Candidates - AngelList')


    def connect(self, limit=50):
        count = 0
        prevTitles = []

        while count < 50:
            btns = self._mClass('interested-button')
            for btn in btns:
                print count
                btn.click()
                count += 1

                sleep(randint(3,5))
