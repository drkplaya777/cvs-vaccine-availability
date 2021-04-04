"""Tests sending emails via gmail"""
import json
import os
import pprint
import unittest.mock as mock
import time

import pytest
from google.oauth2.credentials import Credentials

import tests.common.test_constants as const
from app.csv_vaccine_availability import populate_email_template
from app.gmail.sender_email import (
    load_token, get_token_file_path, save_token, get_gmail_service,
    get_credentials_file_path, create_email, get_email, send_email,
    get_email_subject
)
from app.utils.functions import get_project_root


def test_token_json_file_can_be_found(create_file_json_token):
    token_file = get_token_file_path()

    print(token_file)

    assert os.path.exists(token_file)


def test_credentials_json_file_can_be_found(create_file_json_credentials):

    credentials_file = get_credentials_file_path()

    assert os.path.exists(credentials_file)


def test_Credentials_returned_if_token_file_exists(create_file_json_token):
    token = load_token()

    assert getattr(token, "client_id")
    assert getattr(token, "client_secret")
    assert getattr(token, "scopes")


def test_None_return_if_token_file_doesnt_exist():
    token = load_token()

    assert not token


def test_write_token_writes_a_file_to_project_root():
    mock_credentials = mock.create_autospec(Credentials)
    token_file = {
        "client_id": const.TEST_CLIENT_ID,
        "refresh_token": const.TEST_PROJECT_ID,
        "client_secret": const.TEST_CLIENT_SECRET,
    }
    token_json = json.dumps(token_file, indent=4)
    mock_credentials.to_json.return_value = token_json

    save_token(mock_credentials)

    assert os.path.exists(get_token_file_path())


def test_gmail_inbox_can_list_first_10_emails(monkeypatch):
    root = get_project_root()
    credentials_json_file = os.path.join(root, 'credentials.json')
    monkeypatch.setenv('gmail_credentials_file_path', credentials_json_file)
    max_messages = 10

    service = get_gmail_service()
    result = (service
              .users()
              .messages()
              .list(userId='me', maxResults=max_messages)
              .execute())

    pprint.pprint(result)

    messages = result.get("messages")

    assert len(messages) == max_messages


def test_email_can_be_created(
        set_coder_friendly_email, create_cvs_appointments
):
    appointments = create_cvs_appointments
    email_template = populate_email_template(
        const.TEST_SENDER, appointments,
        const.LAST_CVS_UPDATE)
    from_address = const.MY_EMAIL
    to_address = const.MY_EMAIL
    subject = const.EMAIL_SUBJECT_CSV_AVAILABILITY
    email_body = email_template

    email = create_email(from_address, to_address, subject, email_body)

    assert "raw" in email
    assert isinstance(email['raw'], bytes)


def test_email_can_be_retrieved_from_an_inbox(
        set_coder_friendly_email, create_cvs_appointments,
        set_gmail_credentials_file
):
    appointments = create_cvs_appointments
    email_template = populate_email_template(
        const.TEST_SENDER, appointments,
        const.LAST_CVS_UPDATE)
    from_address = const.MY_EMAIL
    to_address = "walkej19@gmail.com"
    subject = const.EMAIL_SUBJECT_CSV_AVAILABILITY
    email_body = email_template

    email_service = get_gmail_service()
    email_body = create_email(from_address, to_address, subject, email_body)
    user_id = 'me'

    electronic_mail = send_email(email_service, user_id, email_body)

    time.sleep(1)  # give email time to arrive

    sent_email_id = electronic_mail.get('id')
    sent_email = get_email(user_id, sent_email_id, email_service)
    sent_email_subject = get_email_subject(sent_email)

    assert sent_email_subject == subject


if __name__ == '__main__':
    pytest.main()
