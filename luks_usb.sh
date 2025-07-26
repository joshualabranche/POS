#!/bin/bash

# This script will show how to create LUKS formatted disk for USB usage
# Note that you will need to mount and unmount the drive everytime
# Make sure no files are open, processes are running, etc prior to unmounting

# Mounting the Drive:
# $ sudo crytpsetup luksopen $DEVICEPATH $PARTNAME
# $ sudo mount /dev/mapper/$PARTNAME /mnt/$PARTNAME

# Unmounting the Drive:
# $ sudo unmount /mnt/$PARTNAME
# $ sudo cryptsetup luksClose $PARTNAME


# install cryptsetup if not already installed
apt-get install cryptsetup

# list the attached disk drives
fdisk -l

# prompt user for path of the device
read -p '\nEnter the drive path you wish to encrypt: ' DRIVEPATH

# setup the LUKS encryption
echo "Encrypting device at $DRIVEPATH"
while true; do
	read -p "Proceed with action? [Y/n] " yesno
	case $yesno in
		[Yy]* )
			echo "..."
		;;
		[Nn]* )
			echo "Exiting!"
			exit
		;;
		* ) echo "Enter Y/N..."
	esac
done
cryptsetup luksFormat --type luks2 --verify-passphrase $DRIVEPATH

# prompt user for drive partition name
read -p '\nEnter the partition name for the device: ' PARTNAME

# create new partition
cryptsetup luksOpen $DRIVEPATH $PARTNAME

# check the status of the new partition
cryptsetup -v status backup

# create a file system on the new partitions
mkfs -t ext4 -V /dev/mapper/$PARTNAME

# mounting the device to be used
mount /dev/mapper/PARTNAME /mnt/$PARTNAME

echo '\nDevice mounted for file transfer\n'

while true; do
	read -p "Unmount Device? (Y -> unmount, N -> exit script) [Y/n] " yesno
        case $yesno in
                [Yy]* )
                        echo "Unmounting Device"
			umount /mnt/$PARTNAME
			cryptsetup luksClose $PARTNAME

                ;;
                [Nn]* )
                        echo "Exiting!"
                        exit
                ;;
                * ) echo "..."
        esac
done
