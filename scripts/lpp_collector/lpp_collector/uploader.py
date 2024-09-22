from lpp_collector.config import LPP_BASE_URL, LPP_SOURCE_FILES
from lpp_collector.sel_client.models.test_case_result import TestCaseResult
from lpp_collector.sel_client.models.test_case_result_passed import TestCaseResultPassed
from .sel_client.client import Client
from .sel_client.api.default import post_api_testresult_device_id
from .sel_client.models import TestResultRequest
from glob import glob
from _pytest.reports import TestReport


class Uploader:
    def __init__(self, device_id: str):
        self.client = Client(base_url=LPP_BASE_URL)
        self.device_id = device_id
        self.test_results: list[TestCaseResult] = []

    def add_test_result(self, report: TestReport):
        self.test_results.append(
            TestCaseResult(
                name=report.nodeid,
                passed=(
                    TestCaseResultPassed.PASSED
                    if report.passed
                    else TestCaseResultPassed.FAILED
                ),
                message=report.longreprtext,
            )
        )

    def upload(self, source_dir: str, test_dir: str):
        # Find source code files
        source_files = sum(
            [
                glob(f"{source_dir}/**/{pat}", recursive=True)
                for pat in LPP_SOURCE_FILES
            ],
            [],
        )
        print(source_files)
        # Upload test result
        # post_api_testresult_device_id.sync_detailed(
        #     device_id=self.device_id, client=self.client, body=self.result
        # )
