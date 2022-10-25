# twitchio github : https://github.com/TwitchIO/TwitchIO

import os
import json
from twitchio.ext import commands
from openai_api import AI

# Initialise GPT-3
gpt3 = AI()


def write_file(file, content):
    with open(file, 'w') as fp:
        json.dump(content, fp)


def read_file(file):
    try:
        with open(file, 'r') as fp:
            try:
                return json.load(fp)
            except ValueError:
                return
    except FileNotFoundError:
        write_file(file, None)


# Bot init & methods
class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=os.environ['TMI_TOKEN'], prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        await self.connected_channels[0].send('SirUwU BOT IS LIVE SirUwU')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        if message.content.startswith('?'):
            answer = gpt3.ask(message.content[1:], engine='davinci')

            print(gpt3.conversation)

            # await message.channel.send(f'You sent \"{message.content}\" from {message.author.name}')
            await message.channel.send('SirUwU ' + answer)

            # Since we have commands and are overriding the default `event_message`
            # We must let the bot know we want to handle and invoke our commands...
            await self.handle_commands(message)

    async def event_join(self, channel, user):
        known_users = read_file('known_users')
        if known_users is None:
            known_users = list()

        if user.name not in known_users:
            known_users.append(user.name)
            write_file('known_users', known_users)

            await channel.send(f'SirUwU Hi {user.name}, I\'m a super smart Chatbot! Use \"{os.environ["BOT_PREFIX"]}\" at the beginning of your message to \
            chat with me ;)')


if __name__ == "__main__":
    bot = Bot()
    bot.run()
