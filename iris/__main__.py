# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import pytest

restore_terminal_encoding = None
logger = logging.getLogger(__name__)


def main():
    pytest.main(['iris/tests/experiments/test_tabs.py', 'iris/tests/experiments/test_empty.py',  '-vs', '-r s'])
