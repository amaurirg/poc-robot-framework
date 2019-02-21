from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords.browsermanagement import BrowserManagementKeywords
from SeleniumLibrary.utils import (is_truthy)


class GerenciamentoDeBrowser(BrowserManagementKeywords):

    @keyword
    def open_navegador(self, url, browser='firefox', alias=None,
                     remote_url=False, desired_capabilities=None,
                     ff_profile_dir=None):

        if is_truthy(remote_url):
            self.info("Opening browser '%s' to base url '%s' through "
                      "remote server at '%s'." % (browser, url, remote_url))
        else:
            self.info("Opening browser '%s' to base url '%s'." % (browser, url))
        driver = self._make_driver(browser, desired_capabilities,
                                   ff_profile_dir, remote_url)
        try:
            driver.get(url)
        except Exception:
            self.ctx.register_driver(driver, alias)
            self.debug("Opened browser with session id %s but failed "
                       "to open url '%s'." % (driver.session_id, url))
            raise
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return self.ctx.register_driver(driver, alias)
