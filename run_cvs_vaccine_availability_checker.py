"""Need to know if CVS in a given state and city have any COVID
immunization appointments available? Run this file"""
import tests.common.test_constants as const
from app.celery_tasks import check_cvs_for_immunization_availability

if __name__ == '__main__':
    from_address = const.MY_EMAIL
    t_a_ruths_email = "test@gmail.com"
    t_a_ruths_search = {
        'cities': ['MOUNTAIN VIEW', 'SANTA CLARA', 'SAN JOSE', 'PALO ALTO',
                   'FREMONT', 'NEWARK', 'REDWOOD CITY', 'MENLO PARK',
                   'MILPITAS', 'UNION CITY', 'LIVERMORE', 'ALAMEDA',
                   'SAN MATEO'],
        'email': const.MY_EMAIL,
        'recipient_name': 'T.A. Ruth',
        'state': 'CA',
        'to_address': t_a_ruths_email,
        'sleep_time': 600
    }

    bragers_email = 'test@gmail.com'
    bragers_search = {'cities': ['ALBANY', 'TROY', 'WYNANTSKILL', 'SCHENECTADY',
                                 'RENSSELAER', 'COLONIE', 'CLIFTON PARK',
                                 'LATHAM', 'SARATOGA SPRINGS'],
                      'email': const.MY_EMAIL,
                      'recipient_name': 'Brager',
                      'state': const.TEST_STATE_NY,
                      'to_address': bragers_email,
                      'sleep_time': 450}

    bryons_email = 'test@gmail.com'
    bryons_search = {'cities': ['MIDDLETOWN'],
                     'email': const.MY_EMAIL,
                     'recipient_name': 'Karow',
                     'state': const.TEST_STATE_NY,
                     'to_address': bryons_email,
                     'sleep_time': 300}
    helpers = [bragers_search, bryons_search, t_a_ruths_search]

    for detail in helpers:
        subject = const.EMAIL_SUBJECT_CSV_AVAILABILITY
        cities = detail.get('cities')
        to_address = detail.get('to_address')
        recipient_name = detail.get('recipient_name')
        state = detail.get('state')
        one_hour = 3600
        sleep_time = detail.get('sleep_time')

        print(f'Creating job for {recipient_name}')

        check_cvs_for_immunization_availability.apply_async(
            args=[from_address, to_address, subject, cities, recipient_name,
                  state, sleep_time],
            queue="cvs"
        )
