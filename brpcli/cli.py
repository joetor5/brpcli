# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from __version__ import __version__
import sys
import os
import argparse
from btcorerpc.rpc import BitcoinRpc
import btcorerpc.util as rpcutil
import btcoreutil
from termcolor import colored, cprint

BITCOIN_COLOR = (255, 165, 0)

def fprint(func):
    def wrapper(*args, **kwargs):
        rpc_obj = args[0]
        header = func.__name__.capitalize()
        output = func(rpc_obj)

        bcolor_print = lambda x: cprint(x, BITCOIN_COLOR, attrs=["bold"])
        bcolor_print(header)
        bcolor_print("-" * 25)
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
        "sent": [traffic["out"]],
        "recv": [traffic["in"]]
    }

    for tdir in sent_recv:
        tbytes = sent_recv[tdir][0]
        tbytes, tbytes_unit = _get_bytes_conversion(tbytes)

        sent_recv[tdir][0] = tbytes
        sent_recv[tdir].append(tbytes_unit)
    
    return [("Sent", f"{sent_recv['sent'][0]} {sent_recv['sent'][1]}"),
            ("Received", f"{sent_recv['recv'][0]} {sent_recv['recv'][1]}")]

@fprint
def mempool(rpc):
    mempool_info = rpc.get_mem_pool_info()
    mem_usage = round(mempool_info["usage"] / 1000000, 2)
    
    return [("TX Count", f"{mempool_info['size']}"),
            ("Memory Usage", f"{mem_usage} MB")]

@fprint
def blockchain(rpc):
    info = rpc.get_blockchain_info()
    
    blocks = info["blocks"]
    disk_usage, usage_unit = _get_bytes_conversion(info["size_on_disk"])
    progress = round(info["verificationprogress"] * 100)

    data =  [("Block Height", blocks),
            ("Disk Usage", f"{disk_usage} {usage_unit}"),
            ("Progress", f"{progress}%")]

    if info["pruned"]:
        prune_height = info["pruneheight"]
        prune_target, unit = _get_bytes_conversion(info["prune_target_size"])
        data.insert(1, ("Prune Height", prune_height))
        data.insert(2, ("Prune Target", f"{prune_target} {unit}"))

    return data

def print_uptime(rpc):

    uptime_str = rpcutil.get_node_uptime(rpc)

    print(f"Node Uptime: {uptime_str}")

def print_version(rpc):
    version = rpcutil.get_node_version(rpc)

    print(f"Node Version: {version}")

def _get_bytes_conversion(bytes_num):
    conversion = {
        "gb": 1000000000,
        "mb": 1000000
    }

    if bytes_num > conversion["gb"]:
        converted_bytes = round(bytes_num / conversion["gb"], 2)
        unit = "GB"
    else:
        converted_bytes = round(bytes_num / conversion["mb"], 2)
        unit = "MB"

    return converted_bytes, unit

def main():

    parser = argparse.ArgumentParser("brpcli")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("command", type=str, help="command")
    args = parser.parse_args()

    rpc_user, rpc_password = rpc_credentials = btcoreutil.get_bitcoin_rpc_credentials()
    rpc_host = os.getenv("BITCOIN_RPC_HOST")
    if not rpc_host:
        rpc_host = "127.0.0.1"
    
    rpc = BitcoinRpc(rpc_user, rpc_password, rpc_host)

    command_callbacks = {
        "blockchain"    : blockchain,
        "connections"   : connections,
        "traffic"       : traffic,
        "mempool"       : mempool,
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
    print_version(rpc)

if __name__ == "__main__":
    main()

