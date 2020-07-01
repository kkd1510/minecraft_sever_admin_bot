import os
import shutil
import zipfile


def copy_files(source, destination, logger):
        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(destination, item)
            if not os.path.isdir(d):
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            else:
                logger.info(f"Backup at the location {destination} was already created. May be restarting too fast?")

def compress(directory):
    return