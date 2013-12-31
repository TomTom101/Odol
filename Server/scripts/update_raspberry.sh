#!/bin/sh

python setup.py sdist
latest=`ls -t dist/odol* | head -1`
scp $latest pi@192.168.0.18:/home/pi
