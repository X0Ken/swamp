#!/usr/bin/python
import os
import sys
import subprocess
import platform

if __name__ == '__main__':

    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sysstr = platform.system()
    if (sysstr == "Linux"):
        subprocess.Popen(["msgfmt", "-o", "./locale/zh_CN/LC_MESSAGES/i18n.mo",
                          "./locale/zh_CN/LC_MESSAGES/i18n.po"],
                         stdout=subprocess.PIPE)

    from app import app

    sys.exit(app())
