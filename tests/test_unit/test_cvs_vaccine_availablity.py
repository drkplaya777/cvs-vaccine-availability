import pytest

from app.csv_vaccine_availability import create_email_message

TEST_CITY = 'TROY'
TEST_STATE = 'NY'
TEST_SENDER = 'me'


def test_email_message_contains_city_and_status():
    appointment_locations = [(TEST_CITY, TEST_STATE)]

    email_message = create_email_message(TEST_SENDER,
                                         appointment_locations)

    expected_email = """
    
    """

    assert TEST_CITY in email_message
    assert TEST_STATE in email_message


if __name__ == '__main__':
    pytest.main()
