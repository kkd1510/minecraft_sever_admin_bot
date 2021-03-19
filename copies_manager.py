import os
import shutil
import zipfile


def run_copy(source, destination, logger):
    if not os.path.isdir(destination):
        if os.path.isdir(source):
            shutil.copytree(source, destination)

    else:
        logger.info(f"Backup at the location {destination} was already created. May be restarting too fast?")


def list_copies(copies_dir):
    backups = os.listdir(copies_dir)
    backups = [f"{copies_dir}/{copy_name}" for copy_name in backups]
    backups = sorted(backups, key=os.path.getmtime)
    return backups


def compress(directory):
    return