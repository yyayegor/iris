from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Width, height and position of each window are restored."
        self.window_size = None
        self.test_case_id = '114826'
        self.test_suite_id = '1588'
        self.locales = ['en-US']

    def run(self):
        firefox_test_site_tab_pattern = Pattern("firefox_test_site_tab.png")
        focus_test_site_tab_pattern = Pattern("focus_test_site_tab.png")
        focus_test_site_tab_pattern.similarity = 0.95
        iris_pattern = Pattern("iris_tab.png")
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU
        hamburger_menu_quit_item_pattern = Pattern("hamburger_menu_quit_item.png")
        restore_previous_session_pattern = Pattern("restore_previous_session_item.png")
        console_output_height_500 = Pattern("console_output_height_500.png")
        console_output_width_500 = Pattern("console_output_width_500.png")
        console_output_height_400 = Pattern("console_output_height_400.png")
        console_output_width_600 = Pattern("console_output_width_600.png")
        console_output_width_1000 = Pattern("console_output_width_1000.png")

        change_preference("devtools.chrome.enabled", True)

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)

        tab_one_loaded = exists(firefox_test_site_tab_pattern, 10)
        assert_true(self, tab_one_loaded, "First tab loaded")

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)

        tab_two_loaded = exists(focus_test_site_tab_pattern, timeout=1)
        assert_true(self, tab_two_loaded, "Second tab loaded")

        minimize_window()
        open_browser_console()
        type("window.resizeTo(1000, 400)", interval=0.02)
        type(Key.ENTER)
        click_window_control("close")
        default_tabs_position = find(focus_test_site_tab_pattern)
        default_tabs_region = Region(0,
                                     default_tabs_position.y,
                                     width=SCREEN_WIDTH,
                                     height=SCREEN_HEIGHT / 10)
        tab_two_location = find(focus_test_site_tab_pattern)

        tab_two_drop_location = Location(x=0,
                                         y=(tab_two_location.y + 2 * SCREEN_HEIGHT / 5))

        drag_drop(tab_two_location, tab_two_drop_location)
        open_browser_console()
        type("window.resizeTo(600, 400)", interval=0.02)
        type(Key.ENTER)
        click_window_control("close")

        tab_two_relocated = not exists(focus_test_site_tab_pattern, in_region=default_tabs_region)
        assert_true(self, tab_two_relocated, "Second opened tab relocated")
        tab_two_new_location = find(focus_test_site_tab_pattern)

        tab_one_location = find(firefox_test_site_tab_pattern)

        tab_one_drop_location = Location(x=(tab_one_location.x + SCREEN_WIDTH / 5),
                                         y=(tab_one_location.y + SCREEN_HEIGHT / 10))

        drag_drop(tab_one_location, tab_one_drop_location, duration=0.5)
        open_browser_console()
        type("window.resizeTo(500, 500)", interval=0.02)
        type(Key.ENTER)
        click_window_control("close")
        tab_one_drop_location.offset(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 10)

        tab_one_moved = exists(firefox_test_site_tab_pattern)
        assert_true(self, tab_one_moved, "First tab's first relocation completed")
        tab_one_intermediate_location = find(firefox_test_site_tab_pattern)
        drag_drop(tab_one_intermediate_location, tab_one_drop_location, duration=0.5)

        tab_one_relocated = not exists(firefox_test_site_tab_pattern, in_region=default_tabs_region)
        assert_true(self, tab_one_relocated, "First opened tab relocated")
        tab_one_window_region = Region(0,
                                       tab_one_drop_location.y,
                                       width=SCREEN_WIDTH,
                                       height=SCREEN_HEIGHT / 5)

        tab_one_moved_twice = exists(firefox_test_site_tab_pattern)
        assert_true(self, tab_one_moved_twice, "First tab window moved")
        tab_one_new_location = find(firefox_test_site_tab_pattern)
        tab_one_drop_location.left(tab_one_location.x)

        first_window_tab = find(iris_pattern)

        hamburger_menu = find(hamburger_menu_button_pattern, region=tab_one_window_region)
        click(hamburger_menu)
        hamburger_menu_displayed = exists(hamburger_menu_quit_item_pattern)
        assert_true(self, hamburger_menu_displayed, "Hamburger menu displayed")
        exit_item = find(hamburger_menu_quit_item_pattern, )
        click(exit_item, duration=1)

        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url, )

        firefox_restarted = exists(hamburger_menu_button_pattern, timeout=5)
        assert_true(self, firefox_restarted, "Firefox restarted")
        hamburger_menu_new_window = find(hamburger_menu_button_pattern)
        click(hamburger_menu_new_window)
        restore_previous_session_located = exists(restore_previous_session_pattern)
        assert_true(self, restore_previous_session_located, "'Restore previous session' item located")
        restore_previous_session = find(restore_previous_session_pattern)

        click(restore_previous_session)

        session_restored = exists(focus_test_site_tab_pattern)
        assert_true(self, session_restored, "Session restored")

        firefox_test_site_restored_position = find(firefox_test_site_tab_pattern)

        firefox_test_site_restored_coordinates = (firefox_test_site_restored_position.x,
                                                  firefox_test_site_restored_position.y)
        firefox_test_site_old_coordinates = (tab_one_new_location.x,
                                             tab_one_new_location.y)
        assert_equal(self,
                     firefox_test_site_restored_coordinates,
                     firefox_test_site_old_coordinates,
                     "First tab position matched")

        focus_site_restored_position = find(focus_test_site_tab_pattern)
        focus_site_restored_coordinates = (focus_site_restored_position.x,
                                           focus_site_restored_position.y)
        focus_site_old_coordinates = (tab_two_new_location.x,
                                      tab_two_new_location.y)
        assert_equal(self,
                     focus_site_restored_coordinates,
                     focus_site_old_coordinates,
                     "Second tab position matched")

        iris_tab_restored_position = find(iris_pattern)
        iris_tab_restored_coordinates = (iris_tab_restored_position.x,
                                         iris_tab_restored_position.y)
        iris_tab_old_coordinates = (first_window_tab.x,
                                    first_window_tab.y)
        assert_equal(self,
                     iris_tab_restored_coordinates,
                     iris_tab_old_coordinates,
                     "Default iris tab position matched")

        click(firefox_test_site_restored_position, duration=1)
        open_browser_console()
        type("window.innerHeight", interval=0.02)
        type(Key.ENTER)
        test_site_window_height_matched = exists(console_output_height_500)

        type("window.innerWidth", interval=0.02)
        type(Key.ENTER)
        test_site_window_width_matched = exists(console_output_width_500)
        assert_true(self,
                    test_site_window_width_matched and test_site_window_height_matched,
                    "First window size matched")
        click_window_control("close")

        click(focus_site_restored_position, duration=1)
        open_browser_console()
        type("window.innerHeight", interval=0.02)
        type(Key.ENTER)
        focus_site_window_height_matched = exists(console_output_height_400)
        type("window.innerWidth", interval=0.02)
        type(Key.ENTER)
        focus_site_window_width_matched = exists(console_output_width_600)
        assert_true(self,
                    focus_site_window_height_matched and focus_site_window_width_matched,
                    "Second window size matched")
        click_window_control("close")

        click(iris_tab_restored_position)
        open_browser_console()
        type("window.innerHeight", interval=0.02)
        type(Key.ENTER)
        iris_window_height_matched = exists(console_output_height_400)
        type("window.innerWidth", interval=0.02)
        type(Key.ENTER)
        iris_window_width_matched = exists(console_output_width_1000)
        assert_true(self,
                    iris_window_height_matched and iris_window_width_matched,
                    "Iris window size matched")
        click_window_control("close")

        close_window()
        close_window()
