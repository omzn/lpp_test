from lpp_collector.config import LPP_BASE_URL, LPP_SOURCE_FILES
from lpp_collector.sel_client.models.test_case_result import TestCaseResult
from lpp_collector.sel_client.models.test_case_result_passed import TestCaseResultPassed
from lpp_collector.sel_client.types import File, Unset
from .sel_client.client import Client
from .sel_client.api.default import post_api_testresult_device_id
from .sel_client.models import TestResultRequest
from glob import glob
from _pytest.reports import TestReport
import tarfile
from io import BytesIO
from datetime import datetime


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

    def has_any_test_result(self):
        return len(self.test_results) > 0

    def _compress_tar(self, files: list[str]) -> BytesIO:
        tar = BytesIO()
        with tarfile.open(fileobj=tar, mode="w") as tf:
            for file in files:
                tf.add(file)
        return tar

    def upload(self, source_dir: str, test_dir: str, test_type: str):
        # Find source code files
        source_files = sum(
            [
                glob(f"{source_dir}/**/{pat}", recursive=True)
                for pat in LPP_SOURCE_FILES
            ],
            [],
        )

        source_blob = self._compress_tar(source_files)
        source_blob.seek(0)

        result = TestResultRequest(
            device_time=datetime.now(),
            test_type=test_type,
            result=self.test_results,
            testcases=File(payload=BytesIO(), file_name="source.tar"),
            source_code=File(payload=source_blob, file_name="source.tar"),
        )

        # Upload test result
        response = post_api_testresult_device_id.sync_detailed(
            device_id=self.device_id, client=self.client, body=result
        )
        print(response.content.decode())
