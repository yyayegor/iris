# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Previously closed tabs can be restored by using keyboard combinations'
        self.test_case_id = '117047'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        local_url = LocalWeb.FIREFOX_TEST_SITE
        local_url_tab_icon_pattern = Pattern('local_url_tab_icon.png')

        opened_tab_x = []
        for _ in range(5):
            new_tab()
            navigate(local_url)
            website_loaded = exists(LocalWeb.FIREFOX_LOGO, 20)
            assert_true(self, website_loaded,
                        'Website {0} loaded'
                        .format(_+1))
            new_x = find(local_url_tab_icon_pattern).x
            opened_tab_x.append(new_x)

        [close_tab() for _ in range(4)]
        one_tab_exists = exists(LocalWeb.FIREFOX_LOGO, 20)
        assert_true(self, one_tab_exists,
                    '{0} Tabs closed. One opened tab exists.'
                    .format(len(opened_tab_x) - 1))
        i = 0
        for tab_x in opened_tab_x[1:]:  # skip first tab_x, which is opened
            undo_close_tab()
            tab_is_restored = exists(local_url_tab_icon_pattern)
            tab_is_restored_x = find(local_url_tab_icon_pattern).x
            assert_true(self, tab_is_restored,
                        'Tab {0} successfully restored'
                        .format(i+2))
            assert_true(self, tab_x == tab_is_restored_x,
                        'Tab was correctly restored at previous position.')
            i += 1
