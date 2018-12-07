# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Private Browsing session is lost after restarting Firefox'
        self.test_case_id = '107721'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):

        private_browsing_pattern = Pattern('private_browsing.png')
        private_window_inactive_pattern = Pattern('private_window_inactive.png')
        browser_console_title_pattern = Pattern('browser_console_title.png')

        new_private_window()
        private_window_is_loaded = exists(private_browsing_pattern, 20)
        assert_true(self, private_window_is_loaded,
                    'Private windows is loaded')

        if Settings.get_os() == Platform.MAC:
            type(text='j', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
        else:
            type(text='j', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)

        browser_console_opened = exists(browser_console_title_pattern, 20)
        assert_true(self, browser_console_opened,
                    'Browser Console is successfully opened. Browser Console is in focus. Restarting Firefox')

        if Settings.get_os() == Platform.MAC:
            type(text='r', modifier=KeyModifier.CMD + KeyModifier.ALT)
        else:
            type(text='r', modifier=KeyModifier.CTRL + KeyModifier.ALT)

        wait_for_firefox_restart()

        try:
            private_mozilla_closed = wait_vanish(private_window_inactive_pattern, 20)
            assert_true(self, private_mozilla_closed,
                        'Private browsing session is not restored.')
        except FindError:
            raise FindError('Private browser windows was not closed')

        browser_console_active = exists(browser_console_title_pattern, 40)
        assert_true(self, browser_console_active,
                    'Browser Console is active. Closing Browser Console')
        if Settings.get_os() == Platform.MAC:
            type(text='w', modifier=KeyModifier.CMD)
        else:
            type(text=Key.F4, modifier=KeyModifier.ALT)

        try:
            browser_console_closed = wait_vanish(browser_console_title_pattern, 20)
            assert_true(self, browser_console_closed,
                        'Exiting test. Browser console was closed successfully')
        except FindError:
            raise FindError('Browser console was not closed')
