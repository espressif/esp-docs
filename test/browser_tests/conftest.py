import functools
import http.server
import os
import subprocess
import threading

import pytest

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DOXYGEN_EXAMPLE_DIR = os.path.realpath(os.path.join(CURRENT_DIR, '../../examples/doxygen'))
BUILD_DIR = os.path.join(DOXYGEN_EXAMPLE_DIR, '_build/browser_tests')
HTML_DIR = os.path.join(BUILD_DIR, 'en/esp32/html')


@pytest.fixture(scope='session')
def built_docs():
    """Build the doxygen example if not already built. Returns path to HTML dir."""
    if not os.path.exists(os.path.join(HTML_DIR, 'index.html')):
        ret = subprocess.call(
            ['build-docs', '-b', BUILD_DIR, '-t', 'esp32', '-l', 'en', '--project-path', 'src/'],
            cwd=DOXYGEN_EXAMPLE_DIR,
        )
        if ret != 0:
            pytest.fail('Doxygen example build failed — cannot run browser tests')
    return HTML_DIR


@pytest.fixture(scope='session')
def docs_server(built_docs):
    """Serve the built docs over HTTP and yield the base URL.

    fetch() inside hover_api.js requires HTTP — file:// URLs are blocked by
    browsers for cross-origin requests, which is exactly the bug we are testing.
    """
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=built_docs)
    # Silence request logs so test output stays readable
    handler.log_message = lambda *_: None
    server = http.server.HTTPServer(('127.0.0.1', 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f'http://127.0.0.1:{port}'
    server.shutdown()
