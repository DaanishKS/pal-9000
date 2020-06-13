from datetime import date
import json
import logging

from slack import WebClient
from slack.errors import SlackApiError
import pandas as pd


class BirthdayBot:
    def __init__(self, configuration_file, data_file):
        with open(configuration_file, 'r') as fp:
            config_data = json.load(fp)

        slack_token = config_data['bot_user_oauth_token']
        self.client = WebClient(token=slack_token)

        self.birthday_channel = config_data['birthday_channel_id']

        self.data = pd.read_csv(data_file, sep='\t')

    def send_message(self, channel, msg_txt):
        try:
            response = self.client.chat_postMessage(channel=channel,
                                                    text=msg_txt)
        except SlackApiError as e:
            assert e.response["error"]

    def check_bday_eligibility(self):
        today = date.today()
        eligible_people = []

        for n in self.data.itertuples():
            p_month = int(n.birthday[0:2])
            p_day = int(n.birthday[3:5])

            if (today.month == p_month) and (today.day == p_day):
                eligible_people.append(n)

        return eligible_people

    def send_bday_notices(self):
        eligible_people = self.check_bday_eligibility()
        if len(eligible_people) > 0:
            for n in eligible_people:
                if n.last_name[-1] != 's':
                    self.send_message(
                        self.config['test_channel_id'],
                        f"It's {n.first_name} {n.last_name}'s birthday today! :tada:"
                    )
                else:
                    self.send_message(
                        self.config['test_channel_id'],
                        f"It's {n.first_name} {n.last_name}' birthday today! :tada"
                    )
        else:
            logging.info("No birthdays to announce today.")


if __name__ == "__main__":
    logging.basicConfig(filename="history.log", level=logging.DEBUG)
    bot = BirthdayBot("config.json", "data.tsv")
    bot.send_bday_notices()
