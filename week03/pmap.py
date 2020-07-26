#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import subprocess
import shlex
import multiprocessing
import ipaddress
import socket
import functools
import argparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

print_lock = multiprocessing.Lock()


def validate_ip(ip):
    return ipaddress.IPv4Address(ip)


def get_ip_list_in_range(start, end):
    for ips in ipaddress.summarize_address_range(ipaddress.IPv4Address(start), ipaddress.IPv4Address(end)):
        yield from ips


def check_host_with_ping(ip):
    result = subprocess.run(
        shlex.split("ping {ip} -c 3 -t 3".format(ip=str(ip))),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if result.returncode == 0:
        with print_lock:
            print(ip)


def check_port_with_tcp(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3)
    if client.connect_ex((str(host), port)) == 0:
        with print_lock:
            print(port)


def main(args):
    if "ping" == args["f"]:
        ip_list = get_ip_list_in_range(*(validate_ip(ip) for ip in args["ip"].split("-")))
        with ProcessPoolExecutor(args["n"]) as pool:
            pool.map(check_host_with_ping, ip_list)
    elif "tcp" == args["f"]:
        with ThreadPoolExecutor(args["n"]) as pool:
            pool.map(functools.partial(check_port_with_tcp, validate_ip(args["ip"])), range(1, 1025))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="pmap", description="pmap - simulate of nmap")
    parser.add_argument("-n", type=int, nargs="?", required=True)
    parser.add_argument("-f", nargs="?", choices=["ping", "tcp"], required=True)
    parser.add_argument("-ip", nargs="?", required=True)
    args = parser.parse_args()
    main(vars(args))
