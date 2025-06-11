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
        print(func.__name__.capitalize())
        print(("-" * len(func.__name__)) * 2)
        func(args[0])

    return wrapper


@header
def connections(rpc):
    conns = rpcutil.get_node_connections(rpc)
    print(f"Inbound: {conns['in']}")
    print(f"Outbound: {conns['out']}")
    print(f"Total: {conns['total']}")

@header
def traffic(rpc):
    traffic = rpcutil.get_node_traffic(rpc)
    print(f"Received: {traffic['in']}")
    print(f"Sent: {traffic['out']}")


def main(args):

    rpc_user, rpc_password = rpc_credentials = btcoreutil.get_bitcoin_rpc_credentials()
    rpc = BitcoinRpc(rpc_user, rpc_password)

    command_callbacks = {
        "connections"   : connections,
        "traffic"       : traffic
    }

    command_callbacks[args.command](rpc)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("command", type=str, help="command")
    args = parser.parse_args()

    main(args)

