"""Sometimes you just need to refresh a gmail token. This module does just
that by querying for the first 10 emails in a Gmail inbox. The inbox used is
 governed by the `credentials.json` file. """
import os

from app.gmail.sender_email import get_gmail_service
from app.utils.functions import get_project_root

if __name__ == '__main__':
    root = get_project_root()
    credentials_json_file = os.path.join(root, 'credentials.json')

    max_messages = 10

    service = get_gmail_service()
    result = (service
              .users()
              .messages()
              .list(userId='me', maxResults=max_messages)
              .execute())
