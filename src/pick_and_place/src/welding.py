#!/usr/bin/env python3

import subprocess
import sys


def main():
    return subprocess.call(['ros2', 'run', 'pick_and_place', 'pick_and_place_welding', *sys.argv[1:]])


if __name__ == '__main__':
    raise SystemExit(main())
