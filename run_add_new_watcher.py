"""
Need to add a new email and list of cities to the queue? This module is for you!
"""
import click

import tests.common.test_constants as const
from app.celery_tasks import check_cvs_for_immunization_availability


@click.command(help="Run this script to add a new user to the CVS Vaccine "
                    "Availability checker")
@click.argument("name")
@click.argument("email")
@click.argument("cities")
@click.argument("state")
@click.option("--from_address", default="",
              help="email address to send the CVS email from")
@click.option("--subject", default=const.EMAIL_SUBJECT_CSV_AVAILABILITY,
              help="subject of the CVS email")
@click.option("--polling_interval", default=300,
              help="how often should I check for availability")
def add_new_watcher(
        name: str, email: str,  cities: str, state: str,
        from_address: str, subject: str, polling_interval: int
):
    click.echo('Adding new watcher')
    click.echo(f'Recipient name: {name.title()}')
    click.echo(f'Email Address: {email}')
    click.echo(f'State: {state.upper()}')
    click.echo(f'From Email Address: {from_address}')
    click.echo(f'Email subject: {subject}')
    click.echo(f'Polling interval: {polling_interval}')

    cities = explode_cites_into_a_list(cities)

    click.echo(f'Adding {name.title()} to CVS queue')

    check_cvs_for_immunization_availability.apply_async(
        args=[from_address, email, subject, cities, name.title(),
              state.upper(), polling_interval],
        queue="cvs"
    )


def explode_cites_into_a_list(cities: str):
    """Converts a delimited string to a list"""
    click.echo(f'Converting cities to a list')

    explosion = [city.upper() for city in cities.split(";")]

    click.echo(f'Converted cities are {explosion}')

    return explosion


if __name__ == '__main__':
    add_new_watcher()
