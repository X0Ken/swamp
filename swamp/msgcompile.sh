#!/bin/bash

msgfmt -o ./locale/en_US/LC_MESSAGES/i18n.mo \
    ./locale/en_US/LC_MESSAGES/i18n.po
msgfmt -o ./locale/zh_CN/LC_MESSAGES/i18n.mo \
    ./locale/zh_CN/LC_MESSAGES/i18n.po