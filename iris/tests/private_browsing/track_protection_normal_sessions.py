# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking Protection can be activated on Normal sessions as well'
        self.test_case_id = '103329'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def setup(self):
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW

        return

    def run(self):
        privacy_prefs_page_pattern = Pattern('about_preferences_privacy_adress.png')
        always_block_trackers_not_selected_pattern = Pattern('always_block_trackers_not_selected.png')
        always_block_trackers_selected_pattern = Pattern('always_block_trackers_not_selected.png')
        privacy_and_security_tab_pattern = Pattern('privacy_and_security_tab.png')
        cnn_site_logo_pattern = Pattern('cnn_logo.png')
        tracking_protection_shield_pattern = Pattern('tracking_protection_shield.png')

        # Access the about:preferences#privacy page
        navigate('about:preferences#privacy')
        privacy_prefs_page_displayed = exists(privacy_prefs_page_pattern, 3)
        assert_true(self, privacy_prefs_page_displayed, "The privacy preferences page is successfully displayed")

        # Enable the "Always" option from the Tracking Protection section
        always_block_trackers_not_selected_displayed = exists(always_block_trackers_not_selected_pattern, 3)
        if always_block_trackers_not_selected_displayed:
            click(always_block_trackers_not_selected_pattern)

        else:
            raise FindError('Can not find "Always" option from the Tracking Protection')
        privacy_and_security_tab_displayed = exists(privacy_and_security_tab_pattern, 3)
        if privacy_and_security_tab_displayed:
            click(privacy_and_security_tab_pattern)
        else:
            raise FindError('Can not find "Privacy and Security" tab')
        always_block_trackers_selected_displayed = exists(always_block_trackers_selected_pattern, 3)
        assert_true(self, always_block_trackers_selected_displayed,
                    '"Always" option from the Tracking Protection section is enabled')

        # Access the following website
        new_tab()
        navigate('https://edition.cnn.com')
        website_displayed = exists(cnn_site_logo_pattern, 5)
        assert_true(self, website_displayed, 'The Website is successfully displayed')
        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern, 3)
        assert_true(self, tracking_protection_shield_displayed,
                    'The Tracking Protection shield is displayed near the address bar')
