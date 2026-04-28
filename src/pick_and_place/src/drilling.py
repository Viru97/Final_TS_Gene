#!/usr/bin/env python3

import subprocess


def main():
    return subprocess.call(['ros2', 'run', 'pick_and_place', 'pick_and_place_opencv'])


if __name__ == '__main__':
    raise SystemExit(main())
