#/bin/bash

dd if=$1 of=$2 bs=4M conv=fsync status=progress
sync
