"""Fixtures galore!"""
import pytest
import os
import json

from app.utils.functions import get_project_root

import tests.common.test_constants as const


@pytest.fixture
def create_file_json_token():
    """Writes a json test file to the file system"""
    root = get_project_root()
    json_file_path = os.path.join(root, 'token.json')

    token_file = {
        "client_id": const.TEST_CLIENT_ID,
        "refresh_token": const.TEST_PROJECT_ID,
        "client_secret": const.TEST_CLIENT_SECRET,
    }

    token_json = json.dumps(token_file, indent=4)

    with open(json_file_path, "w") as json_file:
        json_file.write(token_json)

    yield json_file_path

    os.remove(json_file_path)
    assert not os.path.exists(json_file_path)


@pytest.fixture
def create_file_json_credentials(monkeypatch):
    """Writes a credentials JSON test file to the file system"""
    root = get_project_root()
    credentials_file_path = os.path.join(root, 'tests', 'common',
                                         'gmail_credentials.json')
    monkeypatch.setenv('gmail_credentials_file_path', credentials_file_path)

    credentials_file = {
        "installed": {
            "client_id": const.TEST_CLIENT_ID,
            "project_id": const.TEST_PROJECT_ID,
            "auth_uri": const.TEST_AUTH_URI,
            "token_uri": const.TEST_TOKEN_URI,
            "auth_provider_x509_cert_url": const.TEST_AUTH_PROVIDER_URL,
            "client_secret": const.TEST_CLIENT_SECRET,
            "redirect_uris": [
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }
    }
    credentials_json = json.dumps(credentials_file, indent=4)

    with open(credentials_file_path, "w") as json_file:
        json_file.write(credentials_json)

    yield credentials_file_path

    os.remove(credentials_file_path)
    assert not os.path.exists(credentials_file_path)


@pytest.fixture
def set_gmail_credentials_file(monkeypatch):
    """Sets the credentials file used to authenticate with the Gmail Api"""
    root = get_project_root()
    credentials_json_file = os.path.join(root, 'credentials.json')

    monkeypatch.setenv('gmail_credentials_file_path', credentials_json_file)


@pytest.fixture
def set_coder_friendly_email(monkeypatch):

    monkeypatch.setenv('friendly_coder_email', const.MY_EMAIL)

    yield


@pytest.fixture
def create_cvs_appointments():
    """Creates CVS fake appointments"""
    appointments = [(const.TEST_CITY_TROY, const.TEST_STATE_NY),
                    (const.TEST_CITY_ALBANY, const.TEST_STATE_NY),
                    (const.TEST_CITY_SCHENECTADY, const.TEST_STATE_NY)]

    yield appointments
