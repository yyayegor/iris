# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check the highlight items when the page is zoomed in/out'
        self.test_case_id = '0'
        self.test_suite_id = '0'
        self.locales = ['en-US']

    def run(self):
        """
        Check the highlight items when the page is zoomed in/out

        STEP 1:
            DESCRIPTION:
                Open Firefox and navigate to a popular website (Google.com, Amazon.com, NYTimes etc).

            EXPECTED:
                The page is successfully loaded.

        STEP 2:
            DESCRIPTION:
                Open the Find toolbar.

            EXPECTED:
                Find Toolbar is opened.

        STEP 3:
            DESCRIPTION:
                Search for a term that appears more than once in the page.

            EXPECTED:
                 All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

        STEP 4:
            DESCRIPTION:
                Zoom the page in/out and check the highlighted items.

            EXPECTED:
                The highlight of the found items doesn't affect the visibility of other words/letters. No misplacement of the highlight is visible


        NOTES:
            Initial version - Dmitry Bakaev  - 14-Nov-2018
            Code review complete - Paul Prokhorov - 15-Nov-2018
        """

        soap_label_pattern = Pattern('soap_label.png')
        see_label_pattern = Pattern('see_label.png')
        see_label_zoom_in_pattern = Pattern('see_label_zoom_in.png')
        see_label_zoom_out_pattern = Pattern('see_label_zoom_out.png')
        see_label_unhighlited_pattern = Pattern('see_label_unhighlited.png')
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')

        """ STEP 1 """

        navigate('https://en.wikipedia.org/wiki/SOAP')
        soap_label_exists = exists(soap_label_pattern, 20)

        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        """ END STEP 1 """

        """ STEP 2 """

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        """ END STEP 2 """

        """ STEP 3 """

        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_pattern, 5)
        unhighlighted_label_exists = exists(see_label_unhighlited_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unhighlighted_label_exists,
                    'The others are not highlighted.')

        """ END STEP 3 """

        """ STEP 4 """

        zoom_in()

        selected_label_exists = exists(see_label_zoom_in_pattern, 5)

        assert_true(self, selected_label_exists,
                    'Zoom in: The highlight of the found items does not affect the visibility of other words/letters')

        zoom_out()
        zoom_out()

        selected_label_exists = exists(see_label_zoom_out_pattern, 5)

        assert_true(self, selected_label_exists,
                    'Zoom out: The highlight of the found items does not affect the visibility of other words/letters')

        """ END STEP 4 """
