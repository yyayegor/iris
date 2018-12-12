from iris.test_case import *


class Test(BaseTest):

    def __init__(self):

        BaseTest.__init__(self)
        self.meta = "Width, height and position of each window are restored."
        self.test_case_id = '114826'
        self.test_suite_id = '1588'
        self.locales = ['en-US']

    def run(self):
        """
        Open new tabs;
        drag the first opened tab from window;
        drag new window lower;
        drag the second opened tab from basic window;
        drag new window aside;
        open hamburger menu;
        click "Quit"/"Exit";
        click "Close Tabs";
        restart firefox;
        restore session;
        check windows;
        """
        firefox_test_site_tab_pattern = Pattern("firefox_test_site_tab.png")
        focus_test_site_tab_pattern = Pattern("focus_test_site_tab.png")
        iris_pattern = Pattern("iris_tab.png")
        hamburger_menu_button_pattern = Pattern("hamburger_menu_button.png")
        hamburger_menu_quit_item_pattern = Pattern("hamburger_menu_quit_item.png")
        close_all_tabs_button_pattern = Pattern("close_all_tabs_button.png")


        time.sleep(3)


        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        tab_1_loaded = exists(firefox_test_site_tab_pattern, 10)
        assert_true(self, tab_1_loaded, "First tab loaded")
        tab_1_location = image_search(firefox_test_site_tab_pattern)

        new_tab()
        navigate(LocalWeb.FOCUS_TEST_SITE)
        tab_2_loaded = exists(focus_test_site_tab_pattern, timeout=1)
        assert_true(self, tab_2_loaded, "Second tab loaded")

        # new_tab()
        # new_tab_location = image_search(new_tab_pattern)
        # window_top_region = Region(x=0, y=(new_tab_location.y - SCREEN_HEIGHT/20),
        #                            width=SCREEN_WIDTH, height=SCREEN_HEIGHT/10)
        # hamburger_menu_button_location = image_search(hamburger_menu_button_pattern, window_top_region)

        tab_1_drop_location = Location(x=tab_1_location.x,
                                       y=(tab_1_location.y + SCREEN_HEIGHT/10))

        drag_drop(tab_1_location, tab_1_drop_location, duration=0.5)
        minimize_window()
        time.sleep(1)
        tab_1_new_location = image_search(firefox_test_site_tab_pattern)
        tab_1_drop_location.left(tab_1_location.x)
        drag_drop(tab_1_new_location, tab_1_drop_location, duration=0.5)
        time.sleep(1)

        tab_2_location = image_search(focus_test_site_tab_pattern)

        tab_2_drop_location = Location(x=(tab_2_location.x + SCREEN_WIDTH / 5),
                                       y=(tab_2_location.y + SCREEN_HEIGHT / 5))

        drag_drop(tab_2_location, tab_2_drop_location)
        minimize_window()
        time.sleep(1)
        tab_2_new_location = image_search(focus_test_site_tab_pattern)
        drag_drop(tab_2_new_location, tab_2_drop_location)
        # hover(Location(SCREEN_WIDTH, SCREEN_HEIGHT), duration=1)
        first_window_tab = image_search(iris_pattern)
        click(first_window_tab)
        minimize_window()
        click(tab_2_drop_location)
        hamburger_menu = image_search(hamburger_menu_button_pattern)
        click(hamburger_menu)
        exit_item = image_search(hamburger_menu_quit_item_pattern)
        click(exit_item, )
        time.sleep(1)
        close_all_tabs_button = image_search(close_all_tabs_button_pattern)
        click(close_all_tabs_button, duration=1.5)
        self.window_size = "200x300"
        restart_firefox(self,
                        self.browser.path,
                        self.profile_path,
                        self.base_local_web_url)
        # minimize_window()

        # click(hamburger_menu_button_location)
        # time.sleep(0.5)
        # click(image_search(hamburger_menu_quit_item_pattern))
        # time.sleep(1)
        # click(image_search(close_all_tabs_button_pattern))
        # restart_firefox(self, )

