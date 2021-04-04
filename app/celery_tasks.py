import time

from app.celery_app import create_celery_app
from app.csv_vaccine_availability import (
    get_vaccine_availability, get_immunization_locations,
    send_cvs_availability_email)

app = create_celery_app()


@app.task
def check_cvs_for_immunization_availability(from_address:str,
                                            to_address: str,
                                            subject: str,
                                            cities: set,
                                            recipient_name: str,
                                            state: str):
    one_hour = 3600

    while True:
        vaccine_availability = get_vaccine_availability(state)

        immunization_locations = get_immunization_locations(
            cities, state, vaccine_availability)

        if immunization_locations.get('available_locations'):

            send_cvs_availability_email(from_address,
                                        to_address,
                                        subject,
                                        immunization_locations,
                                        recipient_name)
            print('CVS availability email sent.')
            print('I go night night now.')
            time.sleep(one_hour)
        else:
            print(f'No availability found in cites {cities}')
            print(f'Trying again in 10 minutes')
            time.sleep(300)
            print('\n')
