#!/bin/bash

xgettext -k_ -o messages.po \
    $(find . -path ./tests -prune -o -name "*.py" -print)
msgmerge -N ./locale/zh_CN/LC_MESSAGES/i18n.po messages.po > new.po
mv new.po ./locale/zh_CN/LC_MESSAGES/i18n.po
rm messages.po