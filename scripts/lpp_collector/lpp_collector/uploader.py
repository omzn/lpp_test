from lpp_collector.config import LPP_BASE_URL, LPP_SOURCE_FILES
from .sel_client.client import Client
from .sel_client.api.default import post_api_testresult_device_id
from .sel_client.models import TestResultRequest
from glob import glob


class Uploader:
    def __init__(self, device_id: str):
        self.client = Client(base_url=LPP_BASE_URL)
        self.device_id = device_id

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
