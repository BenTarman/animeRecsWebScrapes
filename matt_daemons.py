# daemon scripts
import daemon
import argparse
from daemon import pidfile
import time
from myanimelist import get_anime


def start_daemon(pidf):
    # This launches the daemon in its context

    # pidfile is a context
    with daemon.DaemonContext(
            working_directory='/home/bentarman/pythonCodes/animeRecsWebScrapes',
            umask=0o002,
            pidfile=pidfile.TimeoutPIDLockFile(pidf),
    ):
        while True:
            get_anime()


if __name__ == "__main__":
    pid = '/home/bentarman/pythonCodes/animeRecsWebScrapes/get_anime.pid'

    start_daemon(pid)
