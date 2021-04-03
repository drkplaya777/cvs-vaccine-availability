import pprint
import requests
import time
import beepy
import datetime
import jinja2
import os


def create_email_message(name, appointment_locations) -> str:
    """Creates an appointments found email"""
    email_template = f"""
    Howdie do there {name},
    
    The following locations have appointments available 
    {appointment_locations}
    """

    return email_template


def populate_email_template(sender: str, appointments: list,
                            last_cvs_update: str) -> str:
    """Populates a CVS availability email"""
    my_email = os.environ['friendly_coder_email']
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('app', 'templates'),
        autoescape=jinja2.select_autoescape(['html'])
    )
    template = env.get_template('appointments.html')

    appointments.sort()

    last_cvs_update_raw = last_cvs_update
    last_cvs_pretty_date = pretty_up_date(last_cvs_update)

    email_template = template.render(recipient=sender,
                                     locations=appointments,
                                     last_cvs_update_ugly=last_cvs_update_raw,
                                     last_cvs_update_pretty=last_cvs_pretty_date,
                                     my_email=my_email)

    return email_template


def pretty_up_date(ugly_date: str) -> str:
    """Converts a datetime raw into a human readable data"""
    date = datetime.datetime.strptime(ugly_date,
                                      '%Y-%m-%dT%H:%M:%S.%f')
    pretty_date = date.strftime("%c")

    return pretty_date


def submit_request():
    hours_to_run = 3
    max_time = time.time() + hours_to_run * 60 * 60
    state = 'NY'
    mappings = dict()
    appointment_found = False

    while not appointment_found:
        response = requests.get(
            "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo".format(
                state.lower()),
            headers={
                "Referer": "https://www.cvs.com/immunizations/covid-19-vaccine",
            })
        response = response.json()
        payload_data = response['responsePayloadData']['data']
        ny_state = payload_data[state]

        pprint.pprint(response)

        for item in payload_data[state]:
            mappings[item.get('city')] = item.get('status')

        cities = ['ALBANY', 'TROY', 'WYNANTSKILL', 'SCHENECTADY', 'RENSSELAER',
                  'COLONIE', 'CLIFTON PARK', 'LATHAM']
        for city in cities:
            print(city, mappings[city])

        print(
            f"Last updated at: {response['responsePayloadData']['currentTime']}")
        print(f"Last checked at: {datetime.datetime.today()}")
        for city in ny_state:
            if city['city'] in cities and city[
                'status'].upper() != 'FULLY BOOKED':
                print(f"Appointment's {city['status']} found in {city['city']}")
                beepy.beep(sound='coin')
                appointment_found = True
        else:
            print(f'No appointments found in {cities}')

            time.sleep(300)
            print('\n')


if __name__ == '__main__':
    submit_request()
