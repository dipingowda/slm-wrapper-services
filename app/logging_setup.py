import logging 
import sys


class SafeExtraFormatter(logging.Formatter):
    """
    A logging formatter that ensures 'request_id' is always present in the log record.
    If not present, it adds a default value.
    """
    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "request_id"):
            record.request_id = "unknown"
        return super().format(record)

def setup_logging(level :int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(asctime)s %(levelname)s %(name)s [req:%(request_id)s] %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S"

    handler.setFormatter(SafeExtraFormatter(fmt=fmt, datefmt=datefmt))

    """ Third party loggers configuration """
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)

    root.handlers = [handler]


class RequestIDFilter(logging.Filter):
    """
    Ensures every log record has request_id even if middleware didnt set it.
    Access middleware will push request_id into record.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "unknown"
        return True

logging.getLogger().addFilter(RequestIDFilter())


#