import os

LONG_T_BACKUPS = 3


def get_backups(backups_dir):
    backups = os.listdir(backups_dir)
    backups = [f"{backups_dir}/{backup_name}" for backup_name in backups]
    backups = sorted(backups, key=os.path.getmtime)
    long_term_backups = [backups.pop() for _ in range(0, LONG_T_BACKUPS)]
    long_term_backups = sorted(long_term_backups, key=os.path.getmtime)
    long_term_backups_names_only = [os.path.basename(lt_backup_name) for lt_backup_name in long_term_backups]
    return backups, long_term_backups_names_only
