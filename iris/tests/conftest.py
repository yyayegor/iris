import pytest
from iris.api.core.util.core_helper import IrisCore
from iris.firefox.firefox_app import FirefoxApp
from multiprocessing import Process
from iris.local_web_server import LocalWebServer
from iris.api.helpers.general import launch_firefox, quit_firefox
from iris.api.core.util.parse_args import parse_args
from iris.api.helpers.general import confirm_firefox_launch, maximize_window
from iris.api.core.settings import Settings
from iris.api.core.util.core_helper import check_version
import logging

process_list = []
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def browser(request):
    initialize_platform()
    start_local_web_server(parse_args().port)

    def teardown():
        finish(0)

    request.addfinalizer(teardown)
    return FirefoxApp()


def initialize_platform():
    """Initialize platform.

    Fixes the terminal encoding, creating directories, Firefox profiles, report JSONs.
    """
    try:
        IrisCore.create_working_directory()
        IrisCore.create_run_directory()
        IrisCore.create_profile_cache()
    except KeyboardInterrupt:
        finish(1)


@pytest.fixture(scope="function", autouse=True)
def run_iris(request, browser):
    """Runs Iris."""
    marker = request.node.get_closest_marker('compatibility')
    skip_reasons = []
    if marker:
        for name, value in marker.kwargs.iteritems():
            if name == 'exclude':
                if Settings.get_os() in value:
                    skip_reasons.append('excluded for %s' % value)
            if name == 'fx_version':
                if not check_version(browser.version, value):
                    skip_reasons.append(
                        'Current Fx version (%s) does not respect the test condition (%s)' % (browser.version, value))
            if name == 'locale':
                if browser.locale not in value:
                    skip_reasons.append('Unsupported locale')
        if len(skip_reasons) > 0:
            pytest.skip(str(request.node.nodeid) + ' ' + str(skip_reasons))

    firefox_runner = launch_firefox(path=browser.path, url='http://127.0.0.1:%s' % parse_args().port)
    firefox_runner.start()
    confirm_firefox_launch()
    maximize_window()
    yield browser


def finish(code=0):
    """All exit points of Iris need to call this function in order to exit properly."""
    global process_list
    logger.debug('There are %s queued process(es) to terminate.' % len(process_list))
    for process in process_list:
        logger.debug('Terminating process.')
        process.terminate()
        process.join()


def start_local_web_server(port):
    """
    Web servers are spawned in new Process instances, which
    must be saved in a list in order to be terminated later.
    """
    try:
        path = IrisCore.get_local_web_root()
        logger.debug('Starting local web server on port %s for directory %s' % (port, path))
        web_server_process = Process(target=LocalWebServer, args=(path, port,))
        process_list.append(web_server_process)
        web_server_process.start()
    except IOError:
        logger.critical('Unable to launch local web server, aborting Iris.')
