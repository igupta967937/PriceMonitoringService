'''
File name:    mailgun.py
Author:       Martin Dwyer
Date:         April 7, 2020
Description:  This file establishes the Mailgun and MailgunException classes which are utilized along with the
              Mailgun API in order to send emails to users when price limit levels have been reached.
License:      The application is provide herein under the GNU General Public License, a free copyleft license for
              software.  A copy of this license has been provided in the root folder of this application.
'''
import os
from typing import List
from requests import Response, post
from dotenv import load_dotenv

class MailgunException(Exception):
    def __init__(self,message:str):
        self.message = message

class Mailgun:
    @classmethod
    def send_mail(cls,email: List[str], subject: str, text: str, html: str) -> Response:
        load_dotenv()
        messages_folder = os.getenv("MAILGUN_MESSAGES_FOLDER")
        api_key = os.getenv("MAILGUN_API_KEY")
        reply_address = os.getenv("MAILGUN_NO_REPLY")
        print(reply_address)
        response = post(
            messages_folder,
            auth=("api", api_key),
            data={
                "from": reply_address,
                "to": email,
                "subject": subject,
                "text": text,
                "html": html})

        if response.status_code != 200:
            print(response.status_code)
            print(response.json())
            raise MailgunException('An error occurred while sending email')

        else:
            print(response.status_code)

