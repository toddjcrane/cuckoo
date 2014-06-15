#!/usr/bin/env python
# Copyright (C) 2010-2014 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import argparse
import logging
import os.path
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

from lib.cuckoo.common.config import Config
from lib.cuckoo.common.constants import CUCKOO_ROOT
from lib.cuckoo.core.database import Database

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vmname", type=str, help="Name of the Virtual Machine.")
    parser.add_argument("--debug", action="store_true", help="Debug log in case of errors.")
    parser.add_argument("--add", action="store_true", help="Add a Virtual Machine.")
    parser.add_argument("--ip", type=str, help="Static IP Address.")
    parser.add_argument("--platform", type=str, default="windows", help="Guest Operating System.")
    parser.add_argument("--tags", type=str, help="Tags for this Virtual Machine.")
    parser.add_argument("--interface", type=str, help="Sniffer interface for this machine.")
    parser.add_argument("--snapshot", type=str, help="Specific Virtual Machine Snapshot to use.")
    parser.add_argument("--resultserver", type=str, help="IP:Port of the Result Server.")
    args = parser.parse_args()

    logging.basicConfig()
    log = logging.getLogger()

    if args.debug:
        log.setLevel(logging.DEBUG)

    db = Database()

    if args.resultserver:
        resultserver_ip, resultserver_port = args.resultserver.split(":")
    else:
        conf = Config(os.path.join(CUCKOO_ROOT, "conf", "cuckoo.conf"))
        resultserver_ip = conf.resultserver.ip
        resultserver_port = conf.resultserver.port

    if args.add:
        db.add_machine(args.vmname, args.vmname, args.ip, args.platform,
                       args.tags, args.interface, args.snapshot,
                       resultserver_ip, int(resultserver_port))
        db.unlock_machine(args.vmname)

if __name__ == "__main__":
    main()
