import gettext
import sys
import traceback

from swamp.exception import ConfigError


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst


class Config(Singleton):
    data_source = "swamp.data_source.STM32.ADSource"
    with_exit = False

    def load(self, kwargs):
        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise ConfigError
            setattr(self, k, v)


CONF = Config()


def convert_args(args):
    kwargs = {}
    for arg in args:
        if '=' not in arg:
            continue
        k, v = arg.split('=', 1)
        kwargs[k] = v.strip()
    return kwargs


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
    # zh_trans.install(unicode=True)
    print("------------------------------")
    return zh_trans


_ = load_i18n().ugettext


def import_class(import_str):
    """Returns a class from a string including module and class.

    .. versionadded:: 0.3
    """
    mod_str, _sep, class_str = import_str.rpartition('.')
    __import__(mod_str)
    try:
        return getattr(sys.modules[mod_str], class_str)
    except AttributeError:
        raise ImportError('Class %s cannot be found (%s)' %
                          (class_str,
                           traceback.format_exception(*sys.exc_info())))


def import_object(import_str, *args, **kwargs):
    """Import a class and return an instance of it.

    .. versionadded:: 0.3
    """
    return import_class(import_str)(*args, **kwargs)
