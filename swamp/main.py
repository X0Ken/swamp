#!/usr/bin/python
import os
import sys


if __name__ == '__main__':

    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))

    from app import app

    sys.exit(app())
