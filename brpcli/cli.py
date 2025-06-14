# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from __version__ import __version__
import sys
import argparse
from btcorerpc.rpc import BitcoinRpc
import btcorerpc.util as rpcutil
import btcoreutil

def header(func):
    def wrapper(*args, **kwargs):
        rpc_obj = args[0]
        print(func.__name__.capitalize())
        print(("-" * len(func.__name__)) * 2)
        func(rpc_obj)

    return wrapper

@header
def connections(rpc):
    conns = rpcutil.get_node_connections(rpc)
    print(f"Inbound: {conns['in']}")
    print(f"Outbound: {conns['out']}")
    print(f"Total: {conns['total']}\n")

@header
def traffic(rpc):
    traffic = rpcutil.get_node_traffic(rpc)
    conversion = 1000000000
    print(f"Sent: {traffic['out'] / conversion} (GB)")
    print(f"Received: {traffic['in'] / conversion} (GB)\n")

@header
def mempool(rpc):
    mempool_info = rpc.get_mem_pool_info()["result"]
    mem_usage = round(mempool_info["usage"] / 1000000, 2)
    print(f"TX Count: {mempool_info['size']}")
    print(f"Memory Usage: {mem_usage} MB\n")


def print_uptime(rpc):

    def append_s(time_str, time_num):
        if time_num > 1:
            return time_str + "s"
        else:
            return time_str

    uptime = rpc.uptime()["result"]
    uptime_str = ""

    mins = uptime / 60
    hours = mins / 60
    days = int(hours / 24)

    if days > 0:
        uptime_str += f"{str(days)} day"
        uptime_str = append_s(uptime_str, days) + ", "

    if int(hours) > 0:
        hours = (hours - 24 * days)
        uptime_str += f"{str(int(hours))} hour"
        uptime_str = append_s(uptime_str, hours) + ", "

        mins = int((hours - int(hours)) * 60)
        uptime_str += f"{str(mins)} minute"
        uptime_str = append_s(uptime_str, mins)
    else:
        mins = int(mins)
        uptime_str += append_s(f"{str(mins)} minute", mins)

    print(f"Node Uptime: {uptime_str}")

def main(args):

    rpc_user, rpc_password = rpc_credentials = btcoreutil.get_bitcoin_rpc_credentials()
    rpc = BitcoinRpc(rpc_user, rpc_password)

    command_callbacks = {
        "connections"   : connections,
        "traffic"       : traffic,
        "mempool"       : mempool
    }

    if args.command not in command_callbacks and args.command != "stats":
        print(f"error: command not supported: {args.command}")
        print("\nSupported commands:\n")
        print("  stats")
        for cmd in command_callbacks:
            print(f"  {cmd}")
        sys.exit(1)

    if args.command == "stats":
        for cmd in command_callbacks:
            command_callbacks[cmd](rpc)
    else:
        command_callbacks[args.command](rpc)

    print_uptime(rpc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("command", type=str, help="command")
    args = parser.parse_args()

    main(args)

