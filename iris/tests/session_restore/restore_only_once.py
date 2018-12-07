# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Firefox can be set to restore a session only once'
        self.test_case_id = '115423'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        accept_risk_pattern = Pattern('accept_risk.png')
        false_value_no_highlight_pattern = Pattern('false_value_no_highlight.png')
        true_value_highlight_pattern = Pattern('true_value_highlight.png')

        navigate('about:config')
        accept_risk_button_exists = exists(accept_risk_pattern, 20)
        assert_true(self, accept_risk_button_exists,
                    'Accept risk button exists')
        click(accept_risk_pattern, 0.2)
        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)
        about_config_page_loaded = region.exists(false_value_no_highlight_pattern, 10)
        assert_true(self, about_config_page_loaded,
                    'The \'about:config\' page successfully loaded.')

        paste('browser.sessionstore.resume_session_once')
        type(Key.ENTER)
        default_value_exists = region.exists(false_value_no_highlight_pattern, 20)
        assert_true(self, default_value_exists,
                    'The \'browser.sessionstore.resume_session_once\' preference has value \'false\' by default.')
        double_click(false_value_no_highlight_pattern)
        true_value_highlight = region.exists(true_value_highlight_pattern, 10)
        assert_true(self, true_value_highlight,
                    'The \'browser.sessionstore.resume_session_once\' preference has value \'true\' after the '
                    'preference has changed.')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        website_one_loaded = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, website_one_loaded,
                    'Page 1 successfully loaded, firefox logo found.')
        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_two_loaded,
                    'Page 2 successfully loaded, firefox logo found.')

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, website_one_loaded,
                    'Page 1 successfully loaded after restart.')
        previous_tab()
        website_two_loaded = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, website_two_loaded,
                    'Page 2 successfully loaded after restart.')
        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)

        previous_tab()
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, 1)
        assert_false(self, website_one_loaded,
                     'Page 1 was not loaded after second restart.')
        previous_tab()
        website_two_loaded = exists(LocalWeb.MOZILLA_LOGO, 1)
        assert_false(self, website_two_loaded,
                     'Page 2 was not loaded after second restart.')
