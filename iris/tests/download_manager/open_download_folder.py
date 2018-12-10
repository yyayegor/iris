# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.helpers.download_manager_utils import download_file, DownloadFiles
from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Hover behavior.'
        self.test_case_id = '99480'
        self.test_suite_id = '1827'
        self.locales = ['en-US']

    def setup(self):
        """Test case setup

        This overrides the setup method in the BaseTest class, so that it can use a brand new profile.
        """
        BaseTest.setup(self)
        self.profile = Profile.BRAND_NEW
        return

    def run(self):
        navigate('https://www.thinkbroadband.com/download')

        # Download a small file.
        download_file(DownloadFiles.EXTRA_SMALL_FILE_5MB, DownloadFiles.OK)

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Downloads button found.')

        expected = exists(DownloadManager.DownloadsPanel.DOWNLOADS_BUTTON, 10)
        assert_true(self, expected, 'Containing folder button is available.')

        # Navigate to Downloads folder.
        click(DownloadManager.DownloadsPanel.OPEN_CONTAINING_FOLDER)

        expected = exists(DownloadManager.DOWNLOADS_FOLDER, 10)
        assert_true(self, expected, 'Downloads folder is displayed.')

        expected = exists(DownloadManager.DownloadsPanel.SMALL_SIZE_FILE_DOWNLOADED, 10)
        assert_true(self, expected, 'Donwloaded file is highlighted.')

        click_window_control('close')

        click(NavBar.DOWNLOADS_BUTTON.target_offset(-70, 15))
