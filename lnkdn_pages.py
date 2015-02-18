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
            profileCards = self._mClass('card-wrapper')

            for profileCard in profileCards:

                # Open the profile in a new tab
                link = profileCard._tag('a')
                self._tmpOpen(link)

                btn = profileCard._css('[data-act="request"]')
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
