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
        iris_pattern = Pattern("iris_tab.png")
        hamburger_menu_button_pattern = Pattern("hamburger_menu_button.png")
        hamburger_menu_quit_item_pattern = Pattern("hamburger_menu_quit_item.png")
        restore_previous_session_pattern = Pattern("restore_previous_session_item.png")

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
        type("window.resizeTo(1900, 400)")
        type(Key.ENTER)
        # type(text=Key.F4, modifier=Key.ALT)
        # close_window()
        click_window_control("close")
        tab_two_location = image_search(focus_test_site_tab_pattern)

        tab_two_drop_location = Location(x=0,
                                         y=(tab_two_location.y + SCREEN_HEIGHT / 5))

        drag_drop(tab_two_location, tab_two_drop_location)
        open_browser_console()
        type("window.resizeTo(600, 400)")
        type(Key.ENTER)
        click_window_control("close")

        exists(focus_test_site_tab_pattern)
        tab_two_new_location = image_search(focus_test_site_tab_pattern)

        tab_one_location = image_search(firefox_test_site_tab_pattern)

        tab_one_drop_location = Location(x=(tab_one_location.x + SCREEN_WIDTH / 5),
                                         y=(tab_one_location.y + SCREEN_HEIGHT / 10))

        drag_drop(tab_one_location, tab_one_drop_location, duration=0.5)
        open_browser_console()
        type("window.resizeTo(500, 500)")
        type(Key.ENTER)
        click_window_control("close")

        exists(firefox_test_site_tab_pattern)
        tab_two_intermediate_location = image_search(firefox_test_site_tab_pattern)
        drag_drop(tab_two_intermediate_location, tab_one_drop_location, duration=0.5)

        tab_one_window_region = Region(tab_one_drop_location.x,
                                       tab_one_drop_location.y,
                                       width=SCREEN_WIDTH,
                                       height=SCREEN_HEIGHT / 5)
        exists(firefox_test_site_tab_pattern)
        tab_one_new_location = image_search(firefox_test_site_tab_pattern)
        tab_one_drop_location.left(tab_one_location.x)
        exists(iris_pattern)
        first_window_tab = image_search(iris_pattern)
        hamburger_menu = image_search(hamburger_menu_button_pattern, region=tab_one_window_region)
        click(hamburger_menu)
        exists(hamburger_menu_quit_item_pattern, )
        exit_item = find(hamburger_menu_quit_item_pattern, )
        click(exit_item, duration=1)

        args = ['-width 400', '-height 400']
        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url,
                        args=args)
        exists(hamburger_menu_button_pattern)
        hamburger_menu_new_window = find(hamburger_menu_button_pattern)
        click(hamburger_menu_new_window)
        exists(restore_previous_session_pattern)
        restore_previous_session = find(restore_previous_session_pattern)

        click(restore_previous_session)
        exists(focus_test_site_tab_pattern)

        firefox_test_site_restored_position = image_search(firefox_test_site_tab_pattern)
        click(firefox_test_site_restored_position, duration=1)

        open_browser_console()
        type("window.innerHeight")
        type(Key.ENTER)
        click_window_control("close")

        firefox_test_site_restored_coordinates = (firefox_test_site_restored_position.x,
                                                  firefox_test_site_restored_position.y)
        firefox_test_site_old_coordinates = (tab_one_new_location.x,
                                             tab_one_new_location.y)
        assert_equal(self,
                     firefox_test_site_restored_coordinates,
                     firefox_test_site_old_coordinates,
                     "First tab position matched")

        focus_site_restored_position = image_search(focus_test_site_tab_pattern)
        focus_site_restored_coordinates = (focus_site_restored_position.x,
                                           focus_site_restored_position.y)
        focus_site_old_coordinates = (tab_two_new_location.x,
                                      tab_two_new_location.y)
        assert_equal(self,
                     focus_site_restored_coordinates,
                     focus_site_old_coordinates,
                     "Second tab position matched")

        iris_tab_restored_position = image_search(iris_pattern)
        iris_tab_restored_coordinates = (iris_tab_restored_position.x,
                                         iris_tab_restored_position.y)
        iris_tab_old_coordinates = (first_window_tab.x,
                                    first_window_tab.y)
        assert_equal(self,
                     iris_tab_restored_coordinates,
                     iris_tab_old_coordinates,
                     "Default iris tab position matched")

        close_window()
        close_window()
