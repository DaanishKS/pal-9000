from datetime import date
import json
import logging
import random

import pandas as pd
from slack import WebClient
from slack.errors import SlackApiError


class Bot:
    def __init__(self, config_file):
        logging.basicConfig(filename="history.log",
                            level=logging.DEBUG,
                            format='%(asctime)s | %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S%z')

        with open(config_file, 'r') as fp:
            self.config = json.load(fp)
        self.api = WebClient(token=self.config['bot_user_token'])

    def send_birthday_notices(self, birthday_data_file, channel_id):
        # Determine who has a birthday today.
        df = pd.read_csv(birthday_data_file, sep='\t')
        today = date.today()
        eligible_people = []

        for n in df.itertuples():
            p_month = int(n.birthday[0:2])
            p_day = int(n.birthday[3:5])

            if (today.month == p_month) and (today.day == p_day):
                eligible_people.append(n)

        # Send out birthday notices.
        msg_template = random.choice(self.config['birthday_messages'])

        if len(eligible_people) > 0:
            for n in eligible_people:
                logging.info(f"Birthday: {n.first_name} {n.last_name}")
                try:
                    msg = msg_template.format(first_name=n.first_name,
                                              last_name=n.last_name)
                    msg = msg.replace("s's", "s'")

                    self.api.chat_postMessage(channel=channel_id, text=msg)

                except SlackApiError as e:
                    assert e.response["error"]

        else:
            logging.info("No birthdays to announce today.")

    def invite_everyone(self, channel_id):
        try:
            response = self.api.users_list()

            user_ids = []
            for user in response['members']:
                if (user['is_bot'] == False) and (user['id'] != "USLACKBOT"):
                    user_ids.append(user['id'])

            self.api.conversations_invite(channel=channel_id, users=user_ids)

        except SlackApiError as e:
            assert e.response["error"]

    def clear_all_messages(self, channel_id):
        try:
            response = self.api.conversations_history(channel=channel_id)

            for msg in response['messages']:
                if 'bot_id' in msg:
                    if msg['bot_id'] == self.config['bot_user_id']:
                        self.api.chat_delete(channel=channel_id, ts=msg['ts'])

        except SlackApiError as e:
            assert e.response["error"]
