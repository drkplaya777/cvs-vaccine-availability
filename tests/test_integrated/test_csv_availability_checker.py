"""Need to test the CVS availability checker? Here ya go!"""
import pytest
import time

from app.csv_vaccine_availability import (
    get_vaccine_availability, get_immunization_locations,
    populate_email_template)
from app.gmail.sender_email import (
    create_email, send_email, get_gmail_service, get_email, get_email_subject)

import tests.common.test_constants as const


def test_availability_can_be_retrieved_from_cvs():
    availability = get_vaccine_availability(state=const.TEST_STATE_NY)

    assert len(availability) > 0


def test_available_immunization_locations_populate_email_template(
        set_coder_friendly_email
):
    cities = {const.TEST_CITY_ALBANY, const.TEST_CITY_TROY,
              const.TEST_CITY_SCHENECTADY}
    vaccine_availability = dict(last_update_time=const.LAST_CVS_UPDATE,
                                data=[{'city': const.TEST_CITY_ALBANY,
                                       'state': const.TEST_STATE_NY,
                                       'status': const.AVAILABLE_STATUS},
                                      {'city': const.TEST_CITY_TROY,
                                       'state': const.TEST_STATE_NY,
                                       'status': const.AVAILABLE_STATUS},
                                      {'city': const.TEST_CITY_SCHENECTADY,
                                       'state': const.TEST_STATE_NY,
                                       'status': const.AVAILABLE_STATUS}])

    immunization_locations = get_immunization_locations(
        cities, const.TEST_STATE_NY, vaccine_availability
    )
    email_template = populate_email_template(
        const.TEST_SENDER, immunization_locations
    )

    assert const.MY_EMAIL in email_template
    assert "Troy, NY" in email_template
    assert "Albany, NY" in email_template
    assert "Schenectady, NY" in email_template


def test_appointment_availability_email_sent(
        set_coder_friendly_email, set_gmail_credentials_file
):
    from_address = const.MY_EMAIL
    to_address = const.MY_EMAIL
    subject = const.EMAIL_SUBJECT_CSV_AVAILABILITY
    cities = {const.TEST_CITY_ALBANY, const.TEST_CITY_TROY,
              const.TEST_CITY_SCHENECTADY}
    vaccine_availability = dict(last_update_time=const.LAST_CVS_UPDATE,
                                data=[{'city': const.TEST_CITY_ALBANY,
                                       'state': const.TEST_STATE_NY,
                                       'status': const.AVAILABLE_STATUS},
                                      {'city': const.TEST_CITY_TROY,
                                       'state': const.TEST_STATE_NY,
                                       'status': const.AVAILABLE_STATUS},
                                      {'city': const.TEST_CITY_SCHENECTADY,
                                       'state': const.TEST_STATE_NY,
                                       'status': const.AVAILABLE_STATUS}])

    immunization_locations = get_immunization_locations(
        cities, const.TEST_STATE_NY, vaccine_availability
    )
    email_template = populate_email_template(
        const.TEST_SENDER, immunization_locations
    )
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
