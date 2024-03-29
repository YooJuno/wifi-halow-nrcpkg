#!/usr/bin/python

import sys
import os
import time
import commands
 
# To probe existing nrc driver and return corresponding insert module command
def insert_module_cmd():
    # Original insert module command
    result = "insmod ./nrc.ko"

    # Change to modprobe command if there were existing nrc driver installed
    ret_code = os.system("modinfo nrc >/dev/null 2>/dev/null")
    if ret_code == 0:
        result = "modprobe nrc"

    return result

def run_newrapeek():
	os.system("sudo killall -9 wireshark-gtk")
	os.system("sudo rmmod nrc")

	os.system("sudo " + insert_module_cmd() + " alternate_mode=1 fw_name=uni_s1g.bin hifspeed=16000000")
	time.sleep(5)

	os.system('sudo ifconfig wlan0 down; sudo iw dev wlan0 set type monitor; sudo ifconfig wlan0 up')

	regstr = "sudo iw reg set " + str(sys.argv[1])
	os.system(regstr)

	cmdstr = "sudo iw dev wlan0 set channel " + str(sys.argv[2])
	os.system(cmdstr)
	time.sleep(3)

	os.system("sudo tshark -i wlan0 -S -l -e wlan.sa -e radiotap.mcs.index -e radiotap.rssi -e radiotap.mcs.gi -Tfields -Y 'wlan.fc.type eq 2' -E header=y ")

total = len(sys.argv)
cmdargs = str(sys.argv)

if total < 3:
	print ("NewraPeek Usage: run_remote.py countrycode channelnumber")
else:
	print ("NewraPeek country code:   %s " % str(sys.argv[1]))
	print ("NewraPeek channel number: %s " % str(sys.argv[2]))
	run_newrapeek()
