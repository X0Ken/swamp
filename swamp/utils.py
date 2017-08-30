import gettext


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


def load_i18n():
    """i18n tools:
    xgettext -k_ -o ./locale/en_US/LC_MESSAGES/i18n.po \
        $(find . -path ./tests -prune -o -name "*.py" -print)
    xgettext -k_ -o ./locale/zh_CN/LC_MESSAGES/i18n.po \
        $(find . -path ./tests -prune -o -name "*.py" -print)

    msgfmt -o ./locale/en_US/LC_MESSAGES/i18n.mo \
        ./locale/en_US/LC_MESSAGES/i18n.po
    msgfmt -o ./locale/zh_CN/LC_MESSAGES/i18n.mo \
        ./locale/zh_CN/LC_MESSAGES/i18n.po
    """
    locale_path = './locale/'
    zh_trans = gettext.translation('i18n', locale_path, languages=['zh_CN'])
    # en_trans = gettext.translation('i18n', locale_path, languages=['en_US'])
    zh_trans.install(unicode=True)
