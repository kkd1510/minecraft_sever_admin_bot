import os
import threading

import discord

from copies_manager import list_copies
from runner import Runner, COPIES_DIR

CMD_PREFIX = '!'

DISCORD_TOKEN = "" # Your bot token here
DISCORD_GUILD = 1234567 # Your server ID here


def get_cmd(cmd_name):
    return f'{CMD_PREFIX}{cmd_name}'


CP_RUN = get_cmd('cp_run')
CP_LIST = get_cmd('cp_list')

client = discord.Client()
backup_runner = Runner()
runner_thread = threading.Thread(target=backup_runner.make_single_copy)
threads_list = [runner_thread]


async def run_cmd(is_any_thread_alive, message):
    if is_any_thread_alive:
        await message.channel.send("Copy already being made!")

    if message.content == CP_RUN:
        runner_thread.start()
        await message.channel.send("Starting copy")

    if message.content == CP_LIST:
        copies = list_copies(COPIES_DIR)
        await message.channel.send(f"There are {len(copies)} copies currently")
        await message.channel.send(f"Copies available:")
        for world_copy in copies:
            await message.channel.send(f"{os.path.basename(world_copy)}")


@client.event
async def on_ready():
    guild = None
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break

    print(f'{client.user} is connected to the following guild:\n'
          f'{guild.name}(id: {guild.id})')


@client.event
async def on_message(message):
    global stopped_previously_flag
    is_any_thread_alive = False

    for backup_t in threads_list:
        if backup_t.is_alive():
            is_any_thread_alive = True

    if message.author == client.user:
        return

    await run_cmd(is_any_thread_alive, message)


client.run(DISCORD_TOKEN)
