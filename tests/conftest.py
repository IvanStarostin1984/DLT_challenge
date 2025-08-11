import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--offline", action="store_true", help="skip tests requiring network"
    )


@pytest.fixture
def offline(request: pytest.FixtureRequest) -> bool:
    return bool(request.config.getoption("--offline"))
