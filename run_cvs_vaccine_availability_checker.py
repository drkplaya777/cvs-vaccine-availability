"""Need to know if CVS in a given state and city have any COVID
immunization appointments available? Run this file"""
import time

from app.csv_vaccine_availability import (
    get_vaccine_availability, get_immunization_locations,
    send_cvs_availability_email)

import tests.common.test_constants as const

if __name__ == '__main__':
    from_address = const.MY_EMAIL
    to_address = const.MY_EMAIL
    subject = const.EMAIL_SUBJECT_CSV_AVAILABILITY
    cities = {const.TEST_CITY_ALBANY, const.TEST_CITY_TROY,
              const.TEST_CITY_SCHENECTADY}
    one_hour = 3600

    while True:
        vaccine_availability = get_vaccine_availability(const.TEST_STATE_NY)

        immunization_locations = get_immunization_locations(
            cities, const.TEST_STATE_NY, vaccine_availability)

        if immunization_locations.get('available_locations'):

            send_cvs_availability_email(from_address,
                                        to_address,
                                        subject,
                                        immunization_locations)
            time.sleep(one_hour)
        else:
            print(f'No available locations found in cites {cities}')
            print(f'Trying again in 10 minutes')
            time.sleep(300)
            print('\n')
