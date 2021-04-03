import pytest

from app.csv_vaccine_availability import populate_email_template, pretty_up_date

TEST_CITY_TROY = 'TROY'
TEST_STATE_NY = 'NY'
TEST_CITY_ALBANY = 'ALBANY'
TEST_CITY_SCHENECTADY = 'SCHENECTADY'
TEST_SENDER = 'me'
LAST_CVS_UPDATE = "2021-04-03T06:56:54.793"
MY_EMAIL = "test@gmail.com"


def test_email_template_includes_sender_name(monkeypatch):
    appointment_locations = [(TEST_CITY_TROY, TEST_STATE_NY)]
    expected = "Howdie do me,"

    monkeypatch.setenv('friendly_coder_email', MY_EMAIL)

    email = populate_email_template(TEST_SENDER, appointment_locations,
                                    LAST_CVS_UPDATE)

    print(email)

    assert expected in email


def test_email_template_includes_cities_and_states(monkeypatch):
    appointments = [(TEST_CITY_TROY, TEST_STATE_NY),
                    (TEST_CITY_ALBANY, TEST_STATE_NY),
                    (TEST_CITY_SCHENECTADY, TEST_STATE_NY)]

    monkeypatch.setenv('friendly_coder_email', MY_EMAIL)

    email = populate_email_template(TEST_SENDER, appointments,
                                    LAST_CVS_UPDATE)

    print(email)

    assert "Troy, NY" in email
    assert "Albany, NY" in email
    assert "Schenectady, NY" in email


def test_pretty_up_date_returns_human_readable_date():
    expected_date = 'Sat Apr  3 06:56:54 2021'

    date = pretty_up_date(LAST_CVS_UPDATE)

    assert date == expected_date


def test_last_cvs_update_included_in_email_template(monkeypatch):
    monkeypatch.setenv('friendly_coder_email', MY_EMAIL)

    appointments = [(TEST_CITY_TROY, TEST_STATE_NY),
                    (TEST_CITY_ALBANY, TEST_STATE_NY),
                    (TEST_CITY_SCHENECTADY, TEST_STATE_NY)]
    expected_date = 'Sat Apr  3 06:56:54 2021 EST'

    email = populate_email_template(TEST_SENDER, appointments, LAST_CVS_UPDATE)

    print(email)

    assert LAST_CVS_UPDATE in email
    assert expected_date in email


def test_my_email_is_included_in_email_template(monkeypatch):
    monkeypatch.setenv('friendly_coder_email', MY_EMAIL)

    appointments = [(TEST_CITY_TROY, TEST_STATE_NY),
                    (TEST_CITY_ALBANY, TEST_STATE_NY),
                    (TEST_CITY_SCHENECTADY, TEST_STATE_NY)]

    email = populate_email_template(TEST_SENDER, appointments, LAST_CVS_UPDATE)

    assert MY_EMAIL in email


if __name__ == '__main__':
    pytest.main()
