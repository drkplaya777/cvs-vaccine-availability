import pytest
import unittest.mock as mock

from app.gmail.sender_email import login_user
import app.gmail.sender_email as func


def test_login_user_refreshes_token_for_expired_credentials(monkeypatch):
    mock_credentials = mock.create_autospec(func.Credentials)
    mock_credentials.expired = "expired"
    mock_credentials.refresh_token = "refresh"
    mock_credentials.valid = False
    mock_Request = mock.create_autospec(func.Request)
    monkeypatch.setattr(func, "Request", mock_Request)
    monkeypatch.setattr(func, 'save_token', mock.MagicMock)
    monkeypatch.setattr(func, 'get_credentials_file_path', mock.MagicMock)

    login_user(mock_credentials)

    assert (mock_credentials.refresh.call_args
            == mock.call(mock_Request.return_value))


def test_login_user_runs_authorization_flow_for_missing_credentials(monkeypatch):
    mock_app_flow = mock.create_autospec(func.InstalledAppFlow)
    monkeypatch.setattr(func, 'InstalledAppFlow', mock_app_flow)
    monkeypatch.setattr(func, 'save_token', mock.MagicMock)
    monkeypatch.setattr(func, 'get_credentials_file_path', mock.MagicMock)

    login_user()

    assert (mock_app_flow.from_client_secrets_file.call_args
            == mock.call("credentials.json", func.SCOPES))


def test_login_user_authorization_runs_local_server_if_no_credentials_provided(
        monkeypatch
):
    mock_app_flow = mock.create_autospec(func.InstalledAppFlow)
    mock_flow = mock_app_flow.from_client_secrets_file.return_value

    monkeypatch.setattr(func, 'InstalledAppFlow', mock_app_flow)
    monkeypatch.setattr(func, 'save_token', mock.MagicMock)
    monkeypatch.setattr(func, 'get_credentials_file_path', mock.MagicMock)

    login_user()

    assert mock_flow.run_local_server.call_args == mock.call(port=0)


def test_login_user_saves_credentials_from_authorization_flow(monkeypatch):
    mock_app_flow = mock.create_autospec(func.InstalledAppFlow)
    mock_flow = mock_app_flow.from_client_secrets_file.return_value
    mock_save_token = mock.create_autospec(func.save_token)
    mock_credentials = mock_flow.run_local_server.return_value

    monkeypatch.setattr(func, 'InstalledAppFlow', mock_app_flow)
    monkeypatch.setattr(func, 'save_token', mock_save_token)
    monkeypatch.setattr(func, 'get_credentials_file_path', mock.MagicMock)

    login_user()

    assert (mock_save_token.call_args
            == mock.call(mock_credentials.to_json.return_value))


def test_login_user_returns_credentials_from_authorization_flow(monkeypatch):
    mock_app_flow = mock.create_autospec(func.InstalledAppFlow)
    mock_flow = mock_app_flow.from_client_secrets_file.return_value
    mock_credentials = mock_flow.run_local_server.return_value

    monkeypatch.setattr(func, 'InstalledAppFlow', mock_app_flow)
    monkeypatch.setattr(func, 'save_token', mock.MagicMock)
    monkeypatch.setattr(func, 'get_credentials_file_path', mock.MagicMock)

    credentials = login_user()

    assert credentials == mock_credentials


def test_login_user_returns_valid_credentials_when_theyre_valid(monkeypatch):
    mock_credentials = mock.create_autospec(func.Credentials)
    mock_credentials.valid = True

    credentials = login_user(mock_credentials)

    assert credentials == mock_credentials


if __name__ == '__main__':
    pytest.main()
