#!/bin/bash

# simple script to wrap daemon processes for easier usage.

# './daemons.sh start get_anime' will start get_anime daemon
# './daemons.sh stop get_anime' will stop the daemon

if [[ $1 = "start" ]]; then
	case $2 in
		get_animes|get_anime|getAnime)
			python3 matt_daemons.py
			;;
	esac


elif [[ $1 = "stop" ]]; then
	case $2 in
		get_animes|get_anime|getAnime)
			start-stop-daemon -K --pidfile get_anime.pid
			;;
	esac

else
	echo 'no valid arg'
fi

