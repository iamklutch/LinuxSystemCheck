#!/usr/bin/env python3

import os
import shutil
import socket
import sys

import psutil


def check_reboot():
    return os.path.exists("/run/reboot-required")


def free_mem():
    # free memory display
    print(os.system("free"))
    return True


def check_for_network():
    """returns True if no network"""
    try:
        print("Checking network status...", end="")
        socket.gethostbyname("google.com")
        print("Success!")
        return False
    except:
        print("Problem with network")
        return True


def check_cpu_high():
    # returns True if CPU is overburdened
    print("Checking CPU usage...")
    return psutil.cpu_percent(1) > 75


def check_disk_full(disk, min_gb, min_percent):
    """returns True if root disk space is below 2 gb"""
    du = shutil.disk_usage(disk)
    # free space calc
    percent_free = 100 * du.free / du.total
    # convert to GB
    gigabytes_free = du.free / 2**30
    print("Disk free space: ", gigabytes_free, "GB")
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    return False


def check_root_full():
    # WRAPPER FUNCITON - checks the root folder size
    return check_disk_full(disk="/", min_gb=2, min_percent=10)


def main():
    """put all checks into a list of tuples to prevent code duplication"""
    checks = [
        (check_reboot, "Pending Reboot."),
        (check_for_network, "No Network"),
        (check_cpu_high, "cpu use over 75%"),
        (check_root_full, "Root Partition has less than 2GB available"),
    ]
    everything_ok = True
    for check, msg in checks:
        # uses the first item in the tuple to run a check and if True return msg
        if check():
            print(msg)
            everything_ok = False

        # if multiple errors, only returns sys error once
        if not everything_ok:
            sys.exit(1)

    print("Everything OK.")
    sys.exit(0)  # doesn't return error msg


free_mem()
main()
