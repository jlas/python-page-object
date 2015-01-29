from sel import AbstractBasePage

class LoginPage(AbstractBasePage):

    def __init__(self, webdriver):
        super(LoginPage, self).__init__(webdriver, 'https://www.linkedin.com/uas/login')

    def signIn(self, email, password):
        emailEl = self._id('session_key-login')
        emailEl.send_keys(email)
        passwordEl = self._id('session_password-login')
        passwordEl.send_keys(password)
        submitEl = self._id('btn-primary')
        submitEl.click()
        return HomePage(self.webdriver)

class HomePage(AbstractBasePage):

    def __init__(self, webdriver):
        super(HomePage, self).__init__(webdriver, 'https://www.linkedin.com/nhome/')


