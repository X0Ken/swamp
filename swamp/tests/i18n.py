# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""
This is a test for i18n.

First:
    xgettext -k_ -o ./locale/en_US/LC_MESSAGES/i18n.po i18n.py
    xgettext -k_ -o ./locale/zh_CN/LC_MESSAGES/i18n.po i18n.py
Next:
    msgfmt -o ./locale/en_US/LC_MESSAGES/i18n.mo i18n.po_en
    msgfmt -o ./locale/zh_CN/LC_MESSAGES/i18n.mo i18n.po_zh
"""

import gettext

locale_path = './locale/'
# gettext.install('internation', locale_path) # 这条语句会将_()函数自动放到python的内置命名空间中
zh_trans = gettext.translation('i18n', locale_path, languages=['zh_CN'])
en_trans = gettext.translation('i18n', locale_path, languages=['en_US'])

print "----中文版本----"
zh_trans.install()
print _("Hello world!")
print _("Python is a good Language.")

print "----英文版本----"
en_trans.install()
print _("Hello world!")
print _("Python is a good Language.")
