#!/bin/sh
### BEGIN INIT INFO
# Provides: service.py
# Required-Start:
# Required-Stop:
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Odol light sensors serial service
# Description:
### END INIT INFO

# chmod +x /etc/init.d/service.sh
# update-rc.d service.sh defaults

case "$1" in
  start)
    log_daemon_msg "Starting kevin_once" &&    
    # Lets make it do something
    /usr/local/bin/status >> /boot/rpi/debug.log &&

    # Okay, now lets remove this script
    rm /etc/init.d/kevin_once &&
    update-rc.d kevin_once remove &&
    log_end_msg $?
    ;;
  *)
    echo "Usage: $0 start" >&2
    exit 3
    ;;
esac