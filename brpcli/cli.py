# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from __version__ import __version__
import sys
import os
import argparse
from btcorerpc.rpc import BitcoinRpc
import btcorerpc.util as rpcutil
import btcoreutil

def fprint(func):
    def wrapper(*args, **kwargs):
        rpc_obj = args[0]
        header = func.__name__.capitalize()
        output = func(rpc_obj)
        print(header)
        print("-" * 25)
        for field, data in output:
            print(f"{field:<15}: {data}")
        print()

    return wrapper

@fprint
def connections(rpc):
    conns = rpcutil.get_node_connections(rpc)
    
    return [("Inbound", conns['in']),
            ("Outbound", conns['out']),
            ("Total", conns['total'])]

@fprint
def traffic(rpc):
    traffic = rpcutil.get_node_traffic(rpc)
    conversion = {
        "gb": 1000000000,
        "mb": 1000000
    }

    sent_recv = {
        "sent": [traffic["out"], "MB"],
        "recv": [traffic["in"], "MB"]
    }

    for tdir in sent_recv:
        tbytes = sent_recv[tdir][0]
        gb_unit = False
        if tbytes > conversion["gb"]:
            num = round(tbytes / conversion["gb"], 2)
            unit = "GB"
            gb_unit = True
        else:
            num = round(tbytes / conversion["mb"], 2)

        sent_recv[tdir][0] = num
        if gb_unit:
            sent_recv[tdir][1] = unit
    
    return [("Sent", f"{sent_recv['sent'][0]} {sent_recv['sent'][1]}"),
            ("Received", f"{sent_recv['recv'][0]} {sent_recv['recv'][1]}")]

@fprint
def mempool(rpc):
    mempool_info = rpc.get_mem_pool_info()["result"]
    mem_usage = round(mempool_info["usage"] / 1000000, 2)
    
    return [("TX Count", f"{mempool_info['size']}"),
            ("Memory Usage", f"{mem_usage} MB")]


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
    rpc_host = os.getenv("BITCOIN_RPC_HOST")
    if not rpc_host:
        rpc_host = "127.0.0.1"
    
    rpc = BitcoinRpc(rpc_user, rpc_password, rpc_host)

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

