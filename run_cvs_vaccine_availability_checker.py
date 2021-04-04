"""Need to know if CVS in a given state and city have any COVID
immunization appointments available? Run this file"""
import tests.common.test_constants as const
from app.celery_tasks import check_cvs_for_immunization_availability

if __name__ == '__main__':
    from_address = const.MY_EMAIL
    to_address = const.MY_EMAIL
    subject = const.EMAIL_SUBJECT_CSV_AVAILABILITY
    cities = [const.TEST_CITY_ALBANY, const.TEST_CITY_TROY,
              const.TEST_CITY_SCHENECTADY]
    recipient_name = const.TEST_RECIPIENT_NAME
    one_hour = 3600

    check_cvs_for_immunization_availability.apply_async(
        args=[from_address, to_address, subject, cities, recipient_name,
              const.TEST_STATE_NY],
        queue="cvs"
    )