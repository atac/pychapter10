import pytest


def pytest_addoption(parser):
    parser.addoption('--file', action='store', default=None,
                     help='Specify a c10 file to test against.')


@pytest.fixture
def f(request):
    return request.config.getoption('--file')
