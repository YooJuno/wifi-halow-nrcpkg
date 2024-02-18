#!/bin/bash

# To probe existing nrc driver and return corresponding insert module command
insert_module_cmd(){
    # Original insert module command
    local result="insmod /home/pi/nrc_pkg/sw/driver/nrc.ko"

    # Change to modprobe command if there were existing nrc driver installed
    if (modinfo nrc >/dev/null 2>/dev/null) ; then
        result="modprobe nrc"
    fi

    echo $result
}

sudo killall -9 hostapd
sudo rmmod nrc
sleep 2
[ -e /lib/firmware/uni_s1g.bin ] || {
sudo cp /home/pi/nrc_pkg/sw/firmware/nrc7292_cspi.bin /lib/firmware/uni_s1g.bin
}
sudo $(insert_module_cmd) power_save=0 fw_name=uni_s1g.bin
sleep 5
sudo ifconfig wlan0 0.0.0.0
sudo ifconfig eth0 0.0.0.0
sleep 5
/home/pi/nrc_pkg/script/cli_app set txpwr 17
sudo hostapd ap_sdk_map.conf -ddddd | tee hostap.log
