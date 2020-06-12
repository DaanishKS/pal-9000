# Birthday Bot

A simple Slack bot that sends out commemorative birthday notices to a specified channel.

## Set-Up

You will need to set up a Slack App and create a bot user. More information can be found on the [API documentation](https://api.slack.com/bot-users#getting-started).

Prior to executing the `birthday_bot.py` script, make sure to create a configuration file called `config.json` and place it in the root folder.

Example of `config.json`:

```json
{
    "bot_user_oauth_token": "xxxx-xxxxxxxxx-xxxx",
    "birthday_channel_id": "C1234567890"
}
```

You will also need a `data.tsv` file containing information on individuals' birthdays. The data in this file will be determine when the bot executes and should also be placed in the root folder.

Example of `data.tsv`:

```tsv
first_name	last_name	birthday
John	Public	10-01
Jane	Doe	03-15
```

Additionally, make sure to create a virtual environment with pipenv:

```shell
cd birthday-bot/
pipenv install
```

## Usage

In order to use this bot script, simply execute `birthday_bot.py` daily. This can be easily automated by adding the following lines to a Crontab:

```
# Run Birthday Bot every day at 2:00 p.m.
0 14 * * * pipenv run python birthday_bot.py
```
