from _pytest.config import Config
from _pytest.reports import TestReport


class LppCollector:
    def __init__(self, config: Config):
        print("LppCollector.__init__() called")

    def pytest_runtest_logreport(self, report: TestReport):
        if report.when == "teardown":
            print(
                "LppCollector.pytest_runtest_logreport() called",
                report.nodeid,
                report.outcome,
            )

    def pytest_collection_modifyitems(self, items):
        print("LppCollector.pytest_collection_modifyitems() called", items)


def pytest_configure(config: Config):  # pragma: no cover
    config.pluginmanager.register(LppCollector(config))
