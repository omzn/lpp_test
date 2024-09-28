import os
from _pytest.config import Config
from _pytest.reports import TestReport

from lpp_collector.config import TARGETPATH

from .uploader import Uploader
from .consent import LppExperimentConsent


class LppCollector:
    def __init__(self, config: Config):
        self.consent = LppExperimentConsent()
        self.uploader = Uploader(device_id="test_device_id")

    def pytest_runtest_logreport(self, report: TestReport):
        if self.consent.get_consent() is None:
            return

        if report.when == "call":
            self.uploader.add_test_result(report)

    def pytest_sessionfinish(self, session, exitstatus):
        if self.consent.get_consent() is None:
            return

        if not self.uploader.has_any_test_result():
            return

        print("Uploading test results...")

        test_type = os.getcwd()

        self.uploader.device_id = self.consent.get_consent()["device_id"]
        self.uploader.upload(source_dir=TARGETPATH, test_dir=".", test_type=test_type)


def pytest_configure(config: Config):  # pragma: no cover
    config.pluginmanager.register(LppCollector(config))
