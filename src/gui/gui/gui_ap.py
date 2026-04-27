#!/usr/bin/env python3
"""Legacy GUI module kept for compatibility.

This module now delegates to the ROS 2 migrated implementation in gui.gui.
"""

from gui.gui import Gui, main

__all__ = ["Gui", "main"]


if __name__ == "__main__":
    raise SystemExit(main())
