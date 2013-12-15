#!/bin/sh

latest=`ls -t dist/odol* | head -1`
python setup.py sdist && scp $latest pi@192.168.0.18:/home/pi
