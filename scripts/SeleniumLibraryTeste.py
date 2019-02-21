# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from SeleniumLibrary.base import DynamicCore
from SeleniumLibrary.errors import NoOpenBrowser
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      FrameKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords,
                                      WebDriverCache,
                                      WindowKeywords,
                                      )
from SeleniumLibrary.locators import ElementFinder
from SeleniumLibrary.utils import Deprecated, LibraryListener, timestr_to_secs
from selenium_library_test import GerenciamentoDeBrowser

__version__ = '3.3.1'


class SeleniumLibraryTeste(DynamicCore):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None):
        """SeleniumLibrary can be imported with several optional arguments.

        - ``timeout``:
          Default value for `timeouts` used with ``Wait ...`` keywords.
        - ``implicit_wait``:
          Default value for `implicit wait` used when locating elements.
        - ``run_on_failure``:
          Default action for the `run-on-failure functionality`.
        - ``screenshot_root_directory``:
          Location where possible screenshots are created. If not given,
          the directory where the log file is written is used.
        """
        self.timeout = timestr_to_secs(timeout)
        self.implicit_wait = timestr_to_secs(implicit_wait)
        self.speed = 0.0
        self.run_on_failure_keyword \
            = RunOnFailureKeywords.resolve_keyword(run_on_failure)
        self._running_on_failure_keyword = False
        self.screenshot_root_directory = screenshot_root_directory
        libraries = [
            GerenciamentoDeBrowser(self),
        ]
        self._drivers = WebDriverCache()
        DynamicCore.__init__(self, libraries)
        self.ROBOT_LIBRARY_LISTENER = LibraryListener()
        self._element_finder = ElementFinder(self)

    _speed_in_secs = Deprecated('_speed_in_secs', 'speed')
    _timeout_in_secs = Deprecated('_timeout_in_secs', 'timeout')
    _implicit_wait_in_secs = Deprecated('_implicit_wait_in_secs',
                                        'implicit_wait')
    _run_on_failure_keyword = Deprecated('_run_on_failure_keyword',
                                         'run_on_failure_keyword')

    def run_keyword(self, name, args, kwargs):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.failure_occurred()
            raise

    def register_driver(self, driver, alias):
        """Add's a `driver` to the library WebDriverCache.

        :param driver: Instance of the Selenium `WebDriver`.
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        :param alias: Alias given for this `WebDriver` instance.
        :type alias: str
        :return: The index of the `WebDriver` instance.
        :rtype: int
        """
        return self._drivers.register(driver, alias)

    def failure_occurred(self):
        """Method that is executed when a SeleniumLibrary keyword fails.

        By default executes the registered run-on-failure keyword.
        Libraries extending SeleniumLibrary can overwrite this hook
        method if they want to provide custom functionality instead.
        """
        if self._running_on_failure_keyword or not self.run_on_failure_keyword:
            return
        try:
            self._running_on_failure_keyword = True
            BuiltIn().run_keyword(self.run_on_failure_keyword)
        except Exception as err:
            logger.warn("Keyword '%s' could not be run on failure: %s"
                        % (self.run_on_failure_keyword, err))
        finally:
            self._running_on_failure_keyword = False

    @property
    def driver(self):
        """Current active driver.

        :rtype: selenium.webdriver.remote.webdriver.WebDriver
        :raises SeleniumLibrary.errors.NoOpenBrowser: If browser is not open.
        """
        if not self._drivers.current:
            raise NoOpenBrowser('No browser is open.')
        return self._drivers.current

    def find_element(self, locator, parent=None):
        """Find element matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: Found `WebElement`.
        :rtype: selenium.webdriver.remote.webelement.WebElement
        :raises SeleniumLibrary.errors.ElementNotFound: If element not found.
        """
        return self._element_finder.find(locator, parent=parent)

    def find_elements(self, locator, parent=None):
        """Find all elements matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: list of found `WebElement` or e,mpty if elements are not found.
        :rtype: list[selenium.webdriver.remote.webelement.WebElement]
        """
        return self._element_finder.find(locator, first_only=False,
                                         required=False, parent=parent)

    @property
    def _cache(self):
        warnings.warn('"SeleniumLibrary._cache" is deprecated, '
                      'use public API instead.', DeprecationWarning)
        return self._drivers

    def _current_browser(self):
        warnings.warn('"SeleniumLibrary._current_browser" is deprecated, '
                      'use "SeleniumLibrary.driver" instead.',
                      DeprecationWarning)
        return self.driver

    def _run_on_failure(self):
        warnings.warn('"SeleniumLibrary._run_on_failure" is deprecated, '
                      'use "SeleniumLibrary.failure_occurred" instead.',
                      DeprecationWarning)
        self.failure_occurred()
