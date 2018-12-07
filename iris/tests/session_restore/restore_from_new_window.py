# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    '''
    1        Launch Firefox with a clean profile.
    Expected result: Firefox successfully launches.

    2        Open some several websites of your choice in different tabs and then close Firefox.
    Expected result: This action is successfully performed.
    Firefox closes successfully.

    3        Open Firefox with the same profile.
    Expected result: Firefox successfully launches.

    4        Open the "Hamburger" menu from a different window.
    Expected result: The "Hamburger" menu is successfully displayed.

    5        Click the "Restore previous session" option.
    Expected result: The recently closed session is successfully restored in the opened window.
    '''

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Session restore can be performed from a new window'
        self.test_case_id = 'C117040'
        self.test_suite_id = '68'
        self.locales = ['en-US']
        self.profile = Profile.LIKE_NEW
        # self.set_profile_pref()

    def run(self):
        url_first = LocalWeb.FIREFOX_TEST_SITE
        url_second = LocalWeb.FIREFOX_TEST_SITE_2

        new_tab()
        navigate(url_first)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded,
                    'Page 1 successfully loaded, firefox logo found.')

        new_tab()
        navigate(url_second)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded,
                    'Page 2 successfully loaded, firefox logo found.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        click_hamburger_menu_option('Restore Previous Session')

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded,
                    'Page 1 successfully restored from previous session.')
        previous_tab()
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded,
                    'Page 2 successfully restored from previous session.')
