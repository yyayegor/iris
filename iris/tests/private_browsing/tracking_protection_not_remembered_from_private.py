from iris.test_case import *


class Test(BaseTest):
    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Tracking protection exceptions can be added but can't be remembered using private browsing session"
        self.test_case_id = "107718"
        self.test_suite_id = "1577"
        self.locales = ['en-US']

    def run(self):
        blocking_turn_off_pattern = Pattern("blocking_turn_off.png")
        cnn_logo_pattern = Pattern("cnn_logo.png")
        empty_exc_list_pattern = Pattern("empty_exc_list.png")
        manage_exceptions_button_pattern = Pattern("manage_exceptions_button.png")
        private_browsing_tab_logo_pattern = Pattern("private_browsing_tab_logo.png")
        tracking_protection_shield_pattern = Pattern("tracking_protection_shield.png")
        tracking_protection_shield_deactivated_pattern = Pattern("tracking_protection_shield_deactivated.png")

        new_private_window()
        private_window_opened = exists(private_browsing_tab_logo_pattern)
        assert_true(self, private_window_opened,
                    "Private window opened")

        navigate("https://edition.cnn.com/?refresh=1")
        tracking_protection_shield_displayed = exists(tracking_protection_shield_pattern,
                                                      timeout=5)
        assert_true(self, tracking_protection_shield_displayed,
                    "Tracking protection shield displayed")
        page_loaded = exists(cnn_logo_pattern, timeout=20)
        assert_true(self, page_loaded,
                    "Page loaded")

        shield_button = find(tracking_protection_shield_pattern)
        click(shield_button)
        protection_popup_opened = exists(blocking_turn_off_pattern)
        assert_true(self, protection_popup_opened,
                    "Protection popup opened")
        turn_off_protection = find(blocking_turn_off_pattern)
        click(turn_off_protection)
        tracking_protection_deactivated = exists(tracking_protection_shield_deactivated_pattern,
                                                 timeout=10)
        assert_true(self, tracking_protection_deactivated,
                    "Tracking protection deactivated")
        close_window()

        new_tab()
        navigate("about:preferences#privacy")
        privacy_prefs_opened = exists(manage_exceptions_button_pattern)
        assert_true(self, privacy_prefs_opened,
                    "Privacy preferences page opened")

        manage_exceptions_button = find(manage_exceptions_button_pattern)
        click(manage_exceptions_button)
        exceptions_window_opened = exists(empty_exc_list_pattern)
        assert_true(self, exceptions_window_opened,
                    "Excepted sites list displayed, it's empty")
