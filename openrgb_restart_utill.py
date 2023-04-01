import os
import time

import psutil
import usb
import tendo.singleton


# get all connected devices
def get_device_pids():
    data = []
    for bus in usb.busses():
        data += [dev.idVendor for dev in bus.devices]
    return data


# get diff between 2 arrays
def get_difference(a: list[int], b: list[int]):
    return list(set(a).symmetric_difference(set(b)))


# stop and start new instance of OpenRGB
def restart_open_rgb():
    for proc in psutil.process_iter():
        if proc.name() == "OpenRGB.exe":
            proc.kill()

    os.startfile('OpenRGB.exe')


try:
    # for one working instance only
    me = tendo.singleton.SingleInstance()
except tendo.singleton.SingleInstanceException:
    print("One instance is running already")
else:
    # loop for checking new devices
    last_pids = None
    while True:
        new_pids = get_device_pids()
        if last_pids is None:
            last_pids = new_pids
            continue

        diff = get_difference(last_pids, new_pids)
        if len(diff) > 0:
            restart_open_rgb()
            print("ready!")
            last_pids = new_pids

        time.sleep(1)
