import logging

from settings import LoggerSettings
from etl import run_etl


logger_settings = LoggerSettings()
logging.basicConfig(level=logger_settings.level)


if __name__ == '__main__':
    run_etl()
