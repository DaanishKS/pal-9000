# PAL 9000

A simple Slack bot that helps manage a workspace.

## Current Functions

+ Send out commemorative birthday notices to a specified channel.
+ Rapidly invite every member in the workspace to a channel.

## Bot Configuration

You will need to set up a Slack App and create a bot user. More information can be found on the [API documentation](https://api.slack.com/bot-users#getting-started).

You will also need to create a configuration file called `_config.json` in the root folder before the bot can be utilized.

Example of minimal `_config.json`:

```json
{
    "bot_user_token": "xxxx-xxxxxxxxx-xxxx"
}
```

Additionally, make sure to create a virtual environment with Pipenv:

```shell
cd birthday-bot/
pipenv install
```

## Birthday Notices

In order for the bot to send out commemorative birthday messages, `_config.json` must be modified to the following:

```json
{
    "bot_user_token": "xxxx-xxxxxxxxx-xxxx",
    "birthday_channel_id": "C1234567890",
    "birthday_messages": [
        "It's {first_name} {last_name}'s birthday today! :tada:"
    ]
}
```

The `birthday_messages` list must include _at least_ one message, which can be anything desired. The individual's first and last name can be included in the message with the terms `{first_name}` and `{last_name}`, respectively. Last names ending with "s" will automatically be accounted when utilizing possessives.

Additionally, a file containing information on individuals' birthdays called `birthdays.tsv` is required. The information in this file will be used to determine when the bot executes this functionality and should also be placed in the root folder.

Example of `birthdays.tsv`:

```tsv
first_name	last_name	birthday
John	Public	10-01
Jane	Doe	03-15
```

Finally, in order to utilize the birthday notices functionality, simply execute `birthday.py` daily. This can be easily automated by adding the following lines to a Crontab file:

```shell
# Run Birthday Bot every day at 2:00 p.m.
0 14 * * * pipenv run python app.py
```
