# Consent state management

import os
import sys

from lpp_collector.docker import fix_permission, run_test_container, update
from .config import (
    IS_DOCKER_ENV,
    LPP_AFTER_CONSENT_TEXT,
    LPP_BASE_URL,
    LPP_DATA_DIR,
    LPP_CONSENT_TEXT,
    LPP_REVOKE_CONSENT_TEXT,
)
from json import load, dump
import typing
from whiptail import Whiptail
from .sel_client import Client
from .sel_client.api.default import post_api_device, delete_api_device_device_id

LPP_CONSENT_FILE = os.path.join(LPP_DATA_DIR, "consent.json")


class ConsentData(typing.TypedDict):
    device_id: str


class LppExperimentConsent:
    def __init__(self):
        self._consent: typing.Optional[ConsentData] = None
        self._load_consent()

    def _load_consent(self):
        try:
            if os.path.exists(LPP_CONSENT_FILE):
                with open(LPP_CONSENT_FILE, "r") as f:
                    self._consent = load(f)
        except Exception as e:
            print(f"Failed to load experiment consent (unexpected error): {e}")

    def get_consent(self):
        return self._consent

    def set_consent(self, consent: ConsentData):
        self._consent = consent
        try:
            with open(LPP_CONSENT_FILE, "w") as f:
                dump(consent, f)
        except Exception as e:
            print(f"Failed to save experiment consent (unexpected error): {e}")

    def delete_consent(self):
        self._consent = None
        os.remove(LPP_CONSENT_FILE)


def show_consent():
    consent_info = LppExperimentConsent()
    current_consent = consent_info.get_consent()

    whiptail = Whiptail(title="Consent Form for experiment")
    client = Client(LPP_BASE_URL)

    if current_consent is not None:
        consent = whiptail.run(
            "yesno",
            LPP_REVOKE_CONSENT_TEXT,
            extra_args=[
                "--scrolltext",
                "--yes-button",
                "同意を取り消す",
                "--no-button",
                "キャンセル",
            ],
        )

        if consent.returncode == 1:
            # Cancelled
            return

        try:
            response = delete_api_device_device_id.sync_detailed(
                current_consent["device_id"],
                client=client,
            )
            if response is None:
                print("同意情報の取り消しに失敗しました")
                return
            consent_info.delete_consent()
            print("同意情報を取り消しました")
        except Exception as e:
            print(f"同意情報の取り消しに失敗しました: {e}")

        return

    # Ask for consent using whiptail
    consent = whiptail.run(
        "yesno",
        LPP_CONSENT_TEXT,
        extra_args=[
            "--scrolltext",
            "--yes-button",
            "同意する",
            "--no-button",
            "同意しない",
        ],
    )

    if consent.returncode == 1:
        # Rejected
        return

    try:
        response = post_api_device.sync(client=client)
        if response is None:
            print("同意情報の送信に失敗しました")
            return
        url = response.consent_form_url
        print(LPP_AFTER_CONSENT_TEXT.format(form_url=url))

        consent_info.set_consent({"device_id": response.device_id})

    except Exception as e:
        print(f"同意情報の送信に失敗しました: {e}")


def main():
    if IS_DOCKER_ENV:
        show_consent()
    else:
        update()
        run_test_container(["lppconsent", *sys.argv[1:]])

    if IS_DOCKER_ENV:
        # Fix permissions
        fix_permission()
