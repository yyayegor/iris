# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *
import sys


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a page with RTL language'
        self.test_case_id = '127251'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        rtl_full_selected_pattern = Pattern('rtl_full_selected.png')
        rtl_deleted_selected_pattern = Pattern('rtl_deleted_selected.png')
        rtl_second_highlighted_pattern = Pattern('rtl_second_highlighted.png')
        rtl_second_not_highlighted_pattern = Pattern('rtl_second_not_highlighted.png')

        test_page_local = self.get_asset_path('rtl.html')
        navigate(test_page_local)

        page_loaded_anchor_exists = exists(rtl_second_not_highlighted_pattern, 20)
        assert_true(self, page_loaded_anchor_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        reload(sys)
        sys.setdefaultencoding('utf8')

        paste('على')

        selected_label_exists = exists(rtl_full_selected_pattern, 1)

        type(Key.BACKSPACE)

        rtl_deleted_selected_exists = exists(rtl_deleted_selected_pattern, 1)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, rtl_deleted_selected_exists,
                    'Typing and deleting work. The caret is placed on the left side of the word.')

        edit_select_all()
        edit_delete()

        paste('ما')

        rtl_second_highlighted_exists = exists(rtl_second_highlighted_pattern, 1)
        rtl_second_not_highlighted_exists = exists(rtl_second_not_highlighted_pattern, 1)

        assert_true(self, rtl_second_highlighted_exists, 'The first one has a green background highlighted.')
        assert_true(self, rtl_second_not_highlighted_exists, 'The second one not highlighted.')

