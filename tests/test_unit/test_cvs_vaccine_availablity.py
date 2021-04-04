import pytest

import tests.common.test_constants as const
from app.csv_vaccine_availability import (
    get_immunization_locations)


def test_appointments_parsed_from_cvs_availability():
    cities = {const.TEST_CITY_ALBANY, const.TEST_CITY_TROY,
              const.TEST_CITY_SCHENECTADY}
    locations = [{'city': const.TEST_CITY_ALBANY,
                  'state': const.TEST_STATE_NY,
                  'status': const.AVAILABLE_STATUS},
                 {'city': const.TEST_CITY_TROY,
                  'state': const.TEST_STATE_NY,
                  'status': const.AVAILABLE_STATUS},
                 {'city': const.TEST_CITY_SCHENECTADY,
                  'state': const.TEST_STATE_NY,
                  'status': const.AVAILABLE_STATUS}]
    vaccine_availability = dict(last_update_time=const.LAST_CVS_UPDATE,
                                data=locations)

    location_data = get_immunization_locations(cities, const.TEST_STATE_NY,
                                               vaccine_availability)

    assert 'last_update' in location_data
    for location in location_data['available_locations']:
        assert location.get('city')
        assert location.get('status')
        assert location.get('state')


if __name__ == '__main__':
    pytest.main()
