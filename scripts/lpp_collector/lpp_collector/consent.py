# Consent state management

import os
from .config import LPP_DATA_DIR, LPP_CONSENT_TEXT
from json import load
import typing
from whiptail import Whiptail

LPP_CONSENT_FILE = os.path.join(LPP_DATA_DIR, "consent.json")


class ConsentData(typing.TypedDict):
    personal_id: str
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
                f.write(consent)
        except Exception as e:
            print(f"Failed to save experiment consent (unexpected error): {e}")

    def delete_consent(self):
        self._consent = None
        os.remove(LPP_CONSENT_FILE)


def main():
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

    print(f"Consent: {consent}")
