import discord
import os
import argparse

from dnd_helper import DNDHelper


class DiscordClient(discord.Client):
    def __init__(self, helper):
        super().__init__()
        self.dnd_helper = helper

    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        userid = message.author.id
        resp = self.dnd_helper.handle_command(userid, message.content)
        if resp:
            await message.channel.send(resp)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--load",
        default="slagthrone",
        help="Load a game by default on start")
    args = parser.parse_args()
    client = DiscordClient(DNDHelper(args.load))
    client.run(os.environ["discord_token"])