#%%
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from typing import List

# If modifying these scopes, delete the file token.json.

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

"""Shows basic usage of the Gmail API.
Lists the user's Gmail labels.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
with open("token.json", "w") as token:
    token.write(creds.to_json())


def get_all_ids() -> List:
    try:
        service = build("gmail", "v1", credentials=creds)
        raw_mess_list = service.users().messages().list(userId="me").execute()
        id_list = []
        for message_info in raw_mess_list['messages']:
            id_list.append(message_info['id'])
        return id_list

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


def get_all_emails(id_list) -> List[dict]:
    try:
        service = build("gmail", "v1", credentials=creds)
        mess_list = []

        for email_id in id_list:
            mess = service.users().messages().get(userId="me", id=email_id).execute()
            email_id = mess["id"]
            if 'data' in mess['payload']['parts'][0]['body']:
                body = base64.urlsafe_b64decode(mess['payload']['parts'][0]['body']['data'].encode("utf-8")).decode(
                    "utf-8")
            else:
                body = ''
            for header in mess['payload']['headers']:
                if header['name'] == 'From':
                    sender = header['value']
                elif header['name'] == 'To':
                    receiver = header['value']
                elif header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'Date':
                    date = header['value']
                else:
                    continue
            formated_mess = {'id': email_id, 'sender': sender, 'receiver': receiver, 'subject': subject, 'date': date,
                             'body': body}
            mess_list.append(formated_mess)

        print(mess_list)
        print(len(mess_list))
        return mess_list
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    id_list = get_all_ids()
    get_all_emails(id_list)
    print("Done")
#%%
