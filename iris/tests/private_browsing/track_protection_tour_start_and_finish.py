# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Tracking protection tour can be successfully started and finished'
        self.test_case_id = '107112'
        self.test_suite_id = '1826'
        self.locales = ['en-US']

    def run(self):
        private_browsing_tab_logo_pattern = Pattern('private_browsing_tab_logo.png')
        see_how_it_works_button_pattern = Pattern('see_how_it_works_button.png')
        new_firefox_content_blocking_label_pattern = Pattern('new_firefox_content_blocking_label.png')
        next_button_first_tour_step_pattern = Pattern('next_button_first_tour_step.png')
        differences_to_expect_label_pattern = Pattern('differences_to_expect_label.png')
        next_button_second_tour_step_pattern = Pattern('next_button_second_tour_step.png')
        turn_off_blocking_label_pattern = Pattern('turn_off_blocking.png')
        got_it_button_pattern = Pattern('got_it_button.png')
        restart_tour_button_pattern = Pattern('restart_tour_button.png')

        # Open a new Private window tab.
        new_private_window()
        private_browsing_tab_logo_displayed = exists(private_browsing_tab_logo_pattern, 5)
        assert_true(self, private_browsing_tab_logo_displayed, "New private window is displayed")

        #  Click the "See how it works" button.
        see_how_it_works_button_displayed = exists(see_how_it_works_button_pattern, 3)
        if see_how_it_works_button_displayed:
            click(see_how_it_works_button_pattern)
        else:
            raise FindError('Can not find the "See how it works" button')

        new_firefox_content_blocking_label_displayed = exists(new_firefox_content_blocking_label_pattern, 5)
        assert_true(self, new_firefox_content_blocking_label_displayed,
                    'The "See how it works" was successfully clicked')

        next_button_first_tour_step_displayed = exists(next_button_first_tour_step_pattern, 3)
        if next_button_first_tour_step_displayed:
            click(next_button_first_tour_step_pattern)
        else:
            raise FindError('Can not find the "Next" button on the first tour step')

        differences_to_expect_label_displayed = exists(differences_to_expect_label_pattern, 5)
        assert_true(self, differences_to_expect_label_displayed, 'The first step of tour is successfully passed')

        next_button_second_tour_step_displayed = exists(next_button_second_tour_step_pattern, 3)
        if next_button_second_tour_step_displayed:
            click(next_button_second_tour_step_pattern)
        else:
            raise FindError('Can not find the "Next" button on the second tour step')

        turn_off_blocking_label_displayed = exists(turn_off_blocking_label_pattern, 5)
        assert_true(self, turn_off_blocking_label_displayed, 'The second step of tour is successfully passed')

        got_it_button_displayed = exists(got_it_button_pattern, 3)
        if got_it_button_displayed:
            click(got_it_button_pattern)
        else:
            raise FindError('Can not find the "Got it!" button')

        restart_tour_button_displayed = exists(restart_tour_button_pattern, 5)
        assert_true(self, restart_tour_button_displayed, 'The tracking protection tour is successfully finished')

        close_window()
