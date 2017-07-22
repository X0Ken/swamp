from  swamp import log

logger = log.get_logger()


class AppException(Exception):
    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                self._log_exception()
                message = self.msg_fmt

        self.message = message
        super(AppException, self).__init__(message)

    def _log_exception(self):
        logger.exception('Exception in string format operation')
        for name, value in self.kwargs.items():
            logger.error("%s: %s" % (name, value))  # noqa

    def format_message(self):
        return self.args[0]


class DataSourceGetError(AppException):
    msg_fmt = "An unknown exception occurred."
