import logging
import os
import sys
import time
import queue

from datetime import datetime

import copy_files
import delete_files

CREATE = 1
DELETE_OLD = 2

SOURCE = "/home/esteban/docker_images/minecraft_server/data/world/"
DESTINATION = "/home/esteban/docker_images/minecraft_world_backups/world_backup"
BACKUPS_DIR = os.path.split(DESTINATION)[0]

START = 'START'
STOP = 'STOP'

LOG_FILENAME = "discord_bot.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logger = logging.getLogger(__name__)
logging_file_handler = logging.FileHandler(LOG_FILENAME)
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(logging_file_handler)
logger.addHandler(console_handler)

class Runner():
    def __init__(self, cmd_queue=None):
        if cmd_queue:
            self.cmd_queue = cmd_queue
        else:
            self.cmd_queue = queue.Queue()

    @staticmethod
    def create_backup():
        now_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        logger.info(f"Creating backup at current time {now_timestamp}")
        copy_files.copy_files(SOURCE, f"{DESTINATION}_{now_timestamp}", logger)


    @staticmethod
    def delete_old_backups():
        delete_files.delete_files(BACKUPS_DIR, logger)

    def run_loop(self):
        activated = True
        last_run_time = time.time()
        Runner.create_backup()
        Runner.delete_old_backups()

        while activated:
            try:
                if self.cmd_queue.get(timeout=1) == STOP:
                    activated = False
                    logger.info("Stopping backup runner now")

            except queue.Empty:
                pass

            elapsed_time = time.time() - last_run_time
            if elapsed_time > 10 * 60:
                last_run_time = time.time()
                Runner.create_backup()
                Runner.delete_old_backups()


if __name__ == "__main__":
    runner = Runner()
    runner.run_loop()
