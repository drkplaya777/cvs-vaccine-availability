import pprint
import requests
import time
import beepy
import datetime
import jinja2
import os
import typing


from app.gmail.sender_email import (
    create_email, send_email, get_gmail_service, get_email, get_email_subject)


def populate_email_template(
        sender: str,
        appointments: typing.Dict,
        recipient_name: str
) -> str:
    """Populates a CVS availability email"""
    last_cvs_update_raw = appointments['last_update']
    last_cvs_pretty_date = pretty_up_date(appointments['last_update'])
    locations = appointments['available_locations']

    my_email = os.environ['friendly_coder_email']
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('app', 'templates'),
        autoescape=jinja2.select_autoescape(['html'])
    )
    template = env.get_template('appointments.html')

    email_template = template.render(recipient=sender,
                                     recipient_name=recipient_name,
                                     locations=locations,
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


def get_vaccine_availability(state: str) -> typing.Dict[str, typing.List[typing.Dict]]:
    """Queries CVS for any availability for vaccine shots!"""
    print('Checking for CVS Availability')
    vaccine_url = (f"https://www.cvs.com/immunizations/"
                   f"covid-19-vaccine.vaccine-status.{state}.json?vaccineinfo")
    cvs_referer = "https://www.cvs.com/immunizations/covid-19-vaccine"
    response = requests.get(vaccine_url,
                            headers={"Referer": cvs_referer})
    response = response.json()
    payload_data = response['responsePayloadData']['data']
    state_data = payload_data[state]
    last_updated_time = response['responsePayloadData']['currentTime']
    print((f"CVS last UPDATED at: "
           f"{response['responsePayloadData']['currentTime']}"))
    print(f"CVS last CHECKED at: {datetime.datetime.today()}")

    return dict(last_update_time=last_updated_time, data=state_data)


def get_immunization_locations(
        cities: set,
        state: str,
        locations: typing.Dict[str, typing.List[typing.Dict]]
) -> typing.Dict[str, typing.List[dict]]:
    """Parses out available locations from a CVS response"""
    print('Filtering out FULLY BOOKED locations')
    immunization_locations = dict()
    filtered_cities = []
    immunization_locations['last_update'] = locations.get('last_update_time')
    immunization_locations['available_locations'] = filtered_cities

    for item in locations['data']:
        if item['city'] in cities and item['status'].upper() != 'FULLY BOOKED':
            print((f"Immunization availability found in {item.get('city')}, "
                   f"{state}"))
            location = (item.get('city'), state)
            filtered_cities.append(location)

    return immunization_locations


def send_cvs_availability_email(
        from_address: str,
        to_address: str,
        subject: str,
        immunization_locations: dict,
        recipient_name: str
):
    """Sends an email via Gmail containing Immunization availability for CVS."""
    print('Sending CVS Availability Email')
    email_template = populate_email_template(
        from_address, immunization_locations, recipient_name
    )
    email_body = email_template

    email_service = get_gmail_service()
    email_body = create_email(from_address, to_address, subject, email_body)
    user_id = 'me'
    electronic_mail = send_email(email_service, user_id, email_body)

    return electronic_mail


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
