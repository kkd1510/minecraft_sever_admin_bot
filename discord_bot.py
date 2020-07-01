import os
import queue
import threading

import discord

from backups_checker import get_backups
from runner import Runner, BACKUPS_DIR, STOP

CMD_PREFIX = '!'

DISCORD_TOKEN = "your_token_here"
DISCORD_GUILD = None # Your guild id here


def get_cmd(cmd_name):
    return f'{CMD_PREFIX}{cmd_name}'


START_CMD = get_cmd('start_backup_runner')
STOP_CMD = get_cmd('stop_backup_runner')
GET_CURRENT_LIST = get_cmd('show_me_the_money')

client = discord.Client()
cmd_queue = queue.Queue()
backup_runner = Runner(cmd_queue)
runner_thread = threading.Thread(target=backup_runner.run_loop)
threads_list = [runner_thread]
stopped_previously_flag = False

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

    if message.content == START_CMD:
        if is_any_thread_alive:
            await message.channel.send("Runner already running!")
        else:
            if stopped_previously_flag:
                new_runner_thread = threading.Thread(target=backup_runner.run_loop)
                threads_list.append(new_runner_thread)
                new_runner_thread.start()
                await message.channel.send("Starting backup runner")
            else:
                runner_thread.start()
                await message.channel.send("Starting backup runner")

    if message.content == STOP_CMD:
        if not is_any_thread_alive:
            await message.channel.send("Runner is currently not running!")
        else:
            stopped_previously_flag = True
            cmd_queue.put(STOP)
            await message.channel.send("Stopping backup runner")

    if message.content == GET_CURRENT_LIST:
        backups, lt_backups = get_backups(BACKUPS_DIR)
        await message.channel.send(f"There are {len(backups) + len(lt_backups)} backups currently")
        await message.channel.send(f"Most recent backups:")
        for lt_backup in lt_backups:
            await message.channel.send(f"{os.path.basename(lt_backup)}")


client.run(DISCORD_TOKEN)
