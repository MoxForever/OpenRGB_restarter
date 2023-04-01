import os
import time

import psutil
import usb


def get_device_pids():
    data = []
    for bus in usb.busses():
        data += [dev.idVendor for dev in bus.devices]
    return data


def get_difference(a: list[int], b: list[int]):
    return list(set(a).symmetric_difference(set(b)))


def restart_open_rgb():
    for proc in psutil.process_iter():
        if proc.name() == "OpenRGB.exe":
            proc.kill()

    os.startfile('OpenRGB.exe')


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
