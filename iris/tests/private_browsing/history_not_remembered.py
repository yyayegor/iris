# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'History is not remembered if reopening a Private window ' \
                    'from the dock (for a profile used only in private mode) '
        self.test_case_id = '101671'
        self.test_suite_id = '1826'
        self.locales = ['en-US']
        self.exclude = [Platform.WINDOWS, Platform.LINUX]

    def run(self):
        soap_label_pattern = Pattern('soap_label.png')
        private_browsing_icon_pattern = Pattern('private_browsing_icon.png')
        new_tab_label_pattern = Pattern('new_tab_label.png')
        firefox_icon_dock_pattern = Pattern('firefox_logo_dock.png')
        wiki_soap_history_icon_pattern = Pattern('wiki_soap_history_icon.png')

        restart_firefox(self,
                        self.browser.path,
                        Profile.LIKE_NEW,
                        '',
                        args=['-private'],
                        image=private_browsing_icon_pattern)

        navigate(LocalWeb.WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        close_window()

        window_closed = exists(soap_label_pattern, 1)
        assert_false(self, window_closed, 'The window is closed')

        firefox_icon_dock_exists = exists(firefox_icon_dock_pattern, 5)
        assert_true(self, firefox_icon_dock_exists, 'The Firefox icon is still visible in the dock.')

        click(firefox_icon_dock_pattern)

        new_window_item_exists = exists(new_tab_label_pattern, 5)
        assert_true(self, new_window_item_exists, 'New window menu item exists.')

        navigate(LocalWeb.WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        history_sidebar()

        type('soap')

        wiki_soap_history_icon_exists = exists(wiki_soap_history_icon_pattern, 2)
        assert_false(self, wiki_soap_history_icon_exists, 'The Recent History section is empty.')
