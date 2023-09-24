def pytest_addoption(parser):
    parser.addoption("--front_url", action="store")
    parser.addoption("--database_url", action="store")
