from bot import Bot

bot = Bot(config_file="_config.json")
bot.send_birthday_notices(birthday_data_file="birthdays.tsv",
                          channel_id=bot.config['birthday_channel_id'])
