# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.local_web import LocalWeb
from iris.api.helpers.general import *
from iris.api.core.util.update_rules import *
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.compatibility(exclude=Platform.MAC, fx_version='>62', locale=['en-US', 'ja'])
def test_tabs():
    new_tab()
    navigate(LocalWeb.MOZILLA_TEST_SITE)
    expected = exists(LocalWeb.MOZILLA_LOGO, 5)
    assert expected, 'Mozilla logo image not found.'

    new_tab()
    navigate(LocalWeb.FIREFOX_TEST_SITE_2)
    expected = exists(LocalWeb.FIREFOX_LOGO, 5)
    assert expected, 'Firefox logo image not found.'

    new_tab()
    navigate(LocalWeb.POCKET_TEST_SITE)
    expected = exists(LocalWeb.POCKET_LOGO, 5)
    assert expected, 'Pocket logo image not found.'

    new_tab()
    navigate(LocalWeb.BLANK_PAGE)

    new_tab()
    new_tab()
    new_tab()
    new_tab()

    navigate(LocalWeb.FOCUS_TEST_SITE)
    expected = exists(LocalWeb.FOCUS_LOGO, 5)
    assert expected, 'Focus logo image not found.'
