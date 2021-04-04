"""
Need to know if your code can send an email? This is the module for you!
"""
import pytest
import os

from app.utils.functions import get_project_root
from app.gmail.sender_email import create_email, send_email
from app.csv_vaccine_availability import populate_email_template

import tests.common.test_constants as const


