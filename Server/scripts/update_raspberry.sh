#!/bin/sh

python setup.py sdist && scp dist/odol-0.1.tar.gz  pi@192.168.0.18:/home/pi
