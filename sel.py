from functools import partial

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def _lookup(multi, by, webdriver, byVal, wait=1, element=None):
    source = element or webdriver
    funcpre = 'find_element_by_'
    if multi:
        funcpre = 'find_elements_by_'
    findByFunc = getattr(source, funcpre+by.replace(' ', '_'))
    if wait is not None:
        w = WebDriverWait(webdriver, wait, poll_frequency=.2)
        try:
            w.until(lambda x: findByFunc(byVal))
        except TimeoutException, e:
            print 'Got TimeoutException waiting on', by, ':', byVal
    try:
        if multi:
            return [ElementWrapper(webdriver, el) for el in findByFunc(byVal)]
        return ElementWrapper(webdriver, findByFunc(byVal))
    except NoSuchElementException, e:
        return None

_lookupId = partial(_lookup, False, By.ID)
_lookupTag = partial(_lookup, False, By.TAG_NAME)
_lookupClass = partial(_lookup, False, By.CLASS_NAME)
_lookupCss = partial(_lookup, False, By.CSS_SELECTOR)
_mLookupId = partial(_lookup, True, By.ID)
_mLookupTag = partial(_lookup, True, By.TAG_NAME)
_mLookupClass = partial(_lookup, True, By.CLASS_NAME)
_mLookupCss = partial(_lookup, True, By.CSS_SELECTOR)


class ElementFinder(object):

    def __init__(self, webdriver, element=None):
        self.webdriver = webdriver
        self.element = element

    def _id(self, _id, wait=1):
        return _lookupId(self.webdriver, _id, wait, self.element)

    def _class(self, _class, wait=1):
        return _lookupClass(self.webdriver, _class, wait, self.element)

    def _tag(self, _tag, wait=1):
        return _lookupTag(self.webdriver, _tag, wait, self.element)

    def _css(self, _css, wait=1):
        return _lookupCss(self.webdriver, _css, wait, self.element)

    def _mId(self, _id, wait=1):
        return _mLookupId(self.webdriver, _id, wait, self.element)

    def _mTag(self, _tag, wait=1):
        return _mLookupTag(self.webdriver, _tag, wait, self.element)

    def _mClass(self, _class, wait=1):
        return _mLookupClass(self.webdriver, _class, wait, self.element)

    def _mCss(self, _css, wait=1):
        return _mLookupCss(self.webdriver, _css, wait, self.element)


class ElementWrapper(ElementFinder):

    def __getattr__(self, name):
        return getattr(self.element, name)


class AbstractBasePage(ElementFinder):

    def __init__(self, webdriver, baseUrl="http://www.example.com"):
        super(AbstractBasePage, self).__init__(webdriver)
        self.baseWin = webdriver.current_window_handle
        self.baseUrl = baseUrl

    def _scrollDown(self):
        self.webdriver.execute_script(
"""
window.scrollTo(0, Math.max(
  document.documentElement.scrollHeight,
  document.body.scrollHeight,
  document.documentElement.clientHeight
));
""")

    def _open(self):
        self.webdriver.get(self.baseUrl)
        return self
