# Consent state management

import os
from .config import LPP_AFTER_CONSENT_TEXT, LPP_BASE_URL, LPP_DATA_DIR, LPP_CONSENT_TEXT
from json import load, dump
import typing
from whiptail import Whiptail
from .sel_client import Client
from .sel_client.api.default import post_api_device

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


def main():
    consent_info = LppExperimentConsent()
    current_consent = consent_info.get_consent()
    if current_consent is not None:
        print("TODO: Implement consent revocation")
        return

    # Ask for consent using whiptail
    whiptail = Whiptail(title="Consent Form for experiment")
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

    client = Client(LPP_BASE_URL)
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
