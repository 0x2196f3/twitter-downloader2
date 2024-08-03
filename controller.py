import os

from apscheduler.schedulers.blocking import BlockingScheduler

import shutil

import main


def is_running_in_docker():
    with open('/proc/1/cgroup', 'r') as f:
        for line in f:
            if 'container' in line:
                return True
    return False


scheduler = BlockingScheduler()

bin_path = "/app"
config_path = "/config"
save_path = "/downloads"


def update_all() -> None:
    os.chdir(bin_path)

    if is_running_in_docker():
        config_file = '/config/settings.json'
        workdir = os.getcwd()
        dest_file = os.path.join(workdir, 'settings.json')

        if os.path.exists(config_file):
            shutil.copy(config_file, dest_file)
            print(f"Copied {config_file} to {dest_file}")
        else:
            print(f"Config file {config_file} not found")
    else:
        print("Not running in Docker, skipping config file copy")

    main.main2()


if __name__ == "__main__":
    update_all()
    interval = os.environ.get('INTERVAL')
    if interval is None or not interval.isdigit():
        interval = 60 * 60 * 12
    else:
        interval = int(interval)

    scheduler.add_job(update_all, 'interval', seconds=interval)
    scheduler.start()
