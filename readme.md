# minecraft_sever_admin_bot
This is a very simple Discord bot that will make a copy of a Minecraft world on the host.

It takes two commands:
- !cp_run - Make a copy of the Minecraft world into the destination folder.
- !cp_list - List the available copies on the destination folder.

##Steps to get running
- Edit the `runner.py` file and change the `SOURCE` and `DESTINATION` constants to the desired values.
- Edit the `discord_bot.py` file and change the `DISCORD_TOKEN` and `DISCORD_GUILD` constants to the desired values.