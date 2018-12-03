# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Private Browsing window is not restored after Firefox crash'
        self.test_case_id = '101748'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.DEFAULT

        return

    def run(self):
        soap_label_pattern = Pattern('soap_label.png')
        private_browsing_icon_pattern = Pattern('private_browsing_icon.png')
        firefox_icon_dock_pattern = Pattern('firefox_logo_dock.png')

        preference_name_label_pattern = Pattern('preference_name_label.png')
        devtools_label_pattern = Pattern('devtools_regular_label.png')
        run_button_pattern = Pattern('run_button.png')
        restore_session_button_pattern = Pattern('restore_session_button.png')
        restart_firefox_button_pattern = Pattern('restart_firefox_button.png')
        mozilla_crash_reporter_label_pattern = Pattern('mozilla_crash_reporter_label.png')
        soap_wikipedia_header_label_pattern = Pattern('soap_wikipedia_header_label.png')
        accept_the_risk_button_pattern = Pattern('accept_the_risk_button.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)
        exists(LocalWeb.FIREFOX_LOGO, 10)

        new_private_window()
        private_browsing_window_opened = exists(private_browsing_icon_pattern, 5)
        assert_true(self, private_browsing_window_opened, 'Private Browsing Window opened')

        navigate(LocalWeb.WIKI_TEST_SITE)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        # crash firefox

        new_tab()
        navigate('about:config')

        accept_the_risk_button_exists = exists(accept_the_risk_button_pattern, 5)
        assert_true(self, accept_the_risk_button_exists, 'Accept the risk button exists.')

        click(accept_the_risk_button_pattern)

        preference_name_label_exists = exists(preference_name_label_pattern, 5)
        assert_true(self, preference_name_label_exists, 'Settings is opened.')

        type('devtools.chrome.enabled')

        devtools_label_exists = exists(devtools_label_pattern, 20)
        assert_true(self, devtools_label_exists, 'Devtools exists.')

        double_click(devtools_label_pattern)
        type(Key.F4, KeyModifier.SHIFT)

        scratchpad_opened = exists(run_button_pattern, 5)
        assert_true(self, scratchpad_opened, 'Scratchpad opened.')

        paste('Cu.import("resource://gre/modules/ctypes.jsm");let zero = new ctypes.intptr_t(8); let badptr = '
              'ctypes.cast(zero, ctypes.PointerType(ctypes.int32_t)); badptr.contents;')
        click(run_button_pattern)

        """
        firefox_crashed = exists(restart_firefox_button_pattern, 10)
        assert_true(self, firefox_crashed, 'Firefox crashed.')

        
        click(restart_firefox_button_pattern)

        # wait
        mozilla_crash_reporter_label_exists = exists(mozilla_crash_reporter_label_pattern, 10)
        assert_true(self, mozilla_crash_reporter_label_exists, 'Crash report windows exists.')

        try:
            crash_report_dismissed = wait_vanish(mozilla_crash_reporter_label_pattern, 10)
            assert_true(self, crash_report_dismissed, 'Crash report dismissed')
        except FindError:
            raise FindError('Crash report is not dismissed')

        firefox_icon_dock_exists = exists(firefox_icon_dock_pattern, 5)
        assert_true(self, firefox_icon_dock_exists, 'Firefox icon exists')
        click(firefox_icon_dock_pattern)

        restore_session_exists = exists(restore_session_button_pattern, 10)
        assert_true(self, restore_session_exists, 'Firefox restored')

        click(restore_session_button_pattern)

        preference_name_label_exists = exists(preference_name_label_pattern, 5)
        assert_true(self, preference_name_label_exists, 'Session is restored.')
        """

        self.firefox_runner = launch_firefox(path=self.browser.path, profile=Profile.DEFAULT, url='about:sessionrestore',
                                             )
        self.firefox_runner.start()

        restore_session_exists = exists(restore_session_button_pattern, 10)
        assert_true(self, restore_session_exists, 'Firefox restored')

        click(restore_session_button_pattern)

        wiki_label_exists = exists(soap_wikipedia_header_label_pattern, 2)
        assert_false(self, wiki_label_exists, 'The Private Browsing window is not restored.')
