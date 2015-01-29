import random
from time import sleep

from selenium.webdriver.common.keys import Keys

from sel import AbstractBasePage

SCRAPE = False

class OkcBasePage(AbstractBasePage):

    def _scrapePics(self):
        pics = []
        for i in xrange(10):
            picId = 'thumb%d' % i
            thumb = self._id(picId)
            if thumb:
                pics.append(thumb._tag('img').get_attribute('src'))
            else:
                break
        return pics

    def _scrapeEssays(self):
        essays = []
        for i in xrange(10):
            essayid = 'essay_%d' % i
            essay = self._id(essayid)
            if essay:
                essayTitle = essay._class('essay_title').text
                essayText = essay._id('essay_text_%d' % i).text
                essays.append({'title': essayTitle, 'text': essayText})
        return essays

    def _scrapeLookingFor(self):
        return {
            'gentation': self._id('ajax_gentation').text,
            'ages': self._id('ajax_ages').text,
            'near': self._id('ajax_near').text,
            'single': self._id('ajax_single').text,
            'relationship': self._id('ajax_lookingfor').text
            }

    def _scrapeStats(self):
        stats = [
            "age",
            "gender",
            "location",
            "orientation",
            "ethnicities",
            "height",
            "bodytype",
            "diet",
            "smoking",
            "drinking",
            "drugs",
            "religion",
            "sign",
            "education",
            "job",
            "income",
            "status",
            "monogamous",
            "children",
            "pets",
            "languages"]
        d = {}
        for stat in stats:
            d[stat] = self._id("ajax_"+stat).text
        d['lastOnline'] = self._css('#profile_details > dl > dd').text
        return d

    def _mongoSetup(self):
        from pymongo import MongoClient
        client = MongoClient()
        db = client['okc']
        self.db = db['users']

    def saveScrapeData(self, data):
        if not hasattr(self, 'db'):
            self._mongoSetup()
        self.db.insert(data)

    def _scrape(self):
        data = {}
        data['pics'] = self._scrapePics()
        data['essays'] = self._scrapeEssays()
        data['lookingFor'] = self._scrapeLookingFor()
        data['stats'] = self._scrapeStats()
        data['name'] = self._id('basic_info_sn').text
        self.saveScrapeData(data)

    def _tmpOpen(self, el, wait=0.2):
        """Open link in new window, then close."""
        el.send_keys(Keys.SHIFT+Keys.RETURN)
        sleep(wait)
        for windowHandle in self.webdriver.window_handles:
            if windowHandle != self.baseWin:
                self.webdriver.switch_to_window(windowHandle)
                if SCRAPE:
                    self._scrape()
                self.webdriver.close()
        self.webdriver.switch_to_window(self.baseWin)


class LoginPage(OkcBasePage):

    def __init__(self, webdriver):
        super(LoginPage, self).__init__(webdriver, 'http://www.okcupid.com')

    def signIn(self, username, password):
        signInEl = self._id('open_sign_in_button')
        signInEl.click()
        usernameEl = self._id('login_username')
        usernameEl.send_keys(username)
        passwordEl = self._id('login_password')
        passwordEl.send_keys(password)
        submitEl = self._id('sign_in_button')
        submitEl.click()
        return HomePage(self.webdriver)


class HomePage(OkcBasePage):

    def __init__(self, webdriver):
        super(HomePage, self).__init__(webdriver, 'http://www.okcupid.com/home')

    def clickBrowseMatches(self):
        browseEl = self._id('nav_matches')
        browseEl._tag('a').click()
        return MatchPage(self.webdriver)


class MatchPage(OkcBasePage):

    def __init__(self, webdriver):
        super(MatchPage, self).__init__(webdriver, 'http://www.okcupid.com/match')

    def visitAllMatches(self, matchLimit=100, randwait=(1,3)):
        matchCount = 0
        while matchCount < matchLimit:
            matchWrap = self._id('match_results')
            matches = matchWrap._mClass('image_wrapper')
            for match in matches[matchCount:]:
                self._tmpOpen(match, wait=random.randint(*randwait))
                matchCount += 1
            self._scrollDown()
