from time import sleep
from random import randint

from sel import AbstractBasePage

class LoginPage(AbstractBasePage):

    def __init__(self, webdriver):
        super(LoginPage, self).__init__(webdriver,
            'https://www.linkedin.com/uas/login', 'Sign In | LinkedIn')

    def signIn(self, email, password):
        emailEl = self._id('session_key-login')
        emailEl.send_keys(email)
        passwordEl = self._id('session_password-login')
        passwordEl.send_keys(password)
        submitEl = self._id('btn-primary')
        submitEl.click()
        hp = HomePage(self.webdriver)
        hp._waitUntilOpen()
        return hp

class HomePage(AbstractBasePage):

    def __init__(self, webdriver):
        super(HomePage, self).__init__(webdriver,
            'https://www.linkedin.com/nhome/', 'Welcome! | LinkedIn')

class PeoplePage(AbstractBasePage):

    def __init__(self, webdriver):
        super(PeoplePage, self).__init__(webdriver,
            'https://www.linkedin.com/people/pymk', 'People You May Know | LinkedIn')

    def connect(self):
        count = 0
        prevTitles = []

        while True:
            connectBtns = self._mCss('[data-act="request"]')
            for btn in connectBtns:
                title = btn.get_attribute('title')

                # Same person? Probably asking for email at this point
                if title in prevTitles:
                    prevTitles = []
                    self._refresh()

                prevTitles.append(title)
                print count, title
                btn.click()
                count += 1

                sleep(randint(3,5))
