from time import sleep
from random import randint

from sel import AbstractBasePage


class LoginPage(AbstractBasePage):

    def __init__(self, webdriver):
        super(LoginPage, self).__init__(webdriver, 'https://members.wework.com/login')

    def signIn(self, email, password):
        emailEl = self._id('email_input')
        emailEl.send_keys(email)
        passwordEl = self._id('password_input')
        passwordEl.send_keys(password)
        submitEl = self._css('[type="submit"]')
        submitEl.click()
        sleep(5)
        hp = HomePage(self.webdriver)
        return hp


class HomePage(AbstractBasePage):

    def __init__(self, webdriver):
        super(HomePage, self).__init__(webdriver, 'https://members.wework.com/')

class DirectoryPage(AbstractBasePage):

    def __init__(self, webdriver):
        super(DirectoryPage, self).__init__(webdriver, 'https://members.wework.com/directory')

    def connect(self):
        count = 0
        prevTitles = []

        while True:
            followBtns = self._mCss('[ng-click="follow(member.uuid)"]')

            for btn in followBtns:

                if btn.text.lower() == 'following':
                    continue

                btn.click()
                count += 1
                print count

                sleep(randint(3,5))
