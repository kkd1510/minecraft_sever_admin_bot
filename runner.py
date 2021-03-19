import logging
import os
import sys

from datetime import datetime

import copies_manager

CREATE = 1
DELETE_OLD = 2

SOURCE = "your_world_path"
DESTINATION = "your_destination_path"
COPIES_DIR = os.path.split(DESTINATION)[0]

LOG_FILENAME = "discord_bot.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logger = logging.getLogger(__name__)
logging_file_handler = logging.FileHandler(LOG_FILENAME)
console_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(logging_file_handler)
logger.addHandler(console_handler)

class Runner():
    def make_single_copy(self):
        now_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        logger.info(f"S_make_single_copy_start_time: {now_timestamp}")
        copies_manager.run_copy(SOURCE, f"{DESTINATION}_{now_timestamp}", logger)
        now_timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        logger.info(f"F_make_single_copy_finish_time: {now_timestamp}")
