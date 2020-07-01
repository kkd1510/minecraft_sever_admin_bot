import os
import shutil

from backups_checker import get_backups

def delete_files(backups_dir, logger, now=False):
    backups, lt_backups = get_backups(backups_dir)
    total_backups_count = len(backups) + len(lt_backups)
    logger.info(f"<=== There are {total_backups_count} backups currently ===>")
    if total_backups_count == 25 or now:
        print("<=== Cleaning up now ===>")
        print(f"Most recent backups:\n {os.path.basename(';'.join(lt_backups))}")
        for backup in backups:
            logger.info(f"Deleting {os.path.basename(backup)}")
            shutil.rmtree(backup)
