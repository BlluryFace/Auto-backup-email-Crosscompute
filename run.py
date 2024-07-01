from pathlib import Path
from sys import argv
import os
import json
import gmail


with open('emails.json', 'w') as f:
    if os.stat('emails.json').st_size == 0:
        id_list = gmail.get_all_ids()
        emails = gmail.get_all_emails(id_list)
        json.dump(emails, f)
    else:
        avai_id = set()
        new_id = list()
        for email in json.load(f):
            avai_id.add(email[id])

        for email_id in gmail.get_all_ids():
            if email_id not in avai_id:
                new_id.append(email_id)
            else: continue

        if not new_id:
            json.load(f).append(gmail.get_all_emails(new_id))
        else:
            f.close()