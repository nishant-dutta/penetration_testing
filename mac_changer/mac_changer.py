#!/usr/bin/env python

import subprocess
import re
import sys
import optparse

# def run_command(command):
#     subprocess.run(command,check=True, shell=True)

def get_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if search_result :
        return search_result.group(0)
    else:
        print(f"[-] No mac address found for interface: {interface}. Exiting ...")
        sys.exit(1)

def change_mac(interface, new_mac_address):
    old_mac_address = get_mac_address(interface)

    if(old_mac_address == new_mac_address):
        print(f"[-] Interface {interface} already has address {new_mac_address}. Exiting ...")
        sys.exit(1)

    print(f"[+] Changing mac address: {get_mac_address(interface)} -> {new_mac_address} for interface: {interface}")

    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac_address])
    subprocess.run(["ifconfig", interface, "up"])

    print("[+] New mac address: " + get_mac_address(interface))

def read_command_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface which needs mac address change")
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address in format -> aa:bb:cc:dd:ee:ff")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info")
    if not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info")

    return options

options = read_command_arguments()
change_mac(options.interface, options.new_mac)