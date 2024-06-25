import datetime
import i18n
import logging
import os
from dotenv import load_dotenv, dotenv_values


class Config:
    def __init__(self):
        load_dotenv()

        [setattr(self, key, value) for key, value in dotenv_values('.env').items()]

    def __getattr__(self, item):
        attr = os.environ.get(item.upper())

        return attr


class Logger:
    def __init__(self, config: Config):
        filename = os.path.dirname(__file__) + '/../storage/logs/{:%Y-%m-%d}.log'.format(datetime.datetime.now())

        logging.basicConfig(
            filename=filename if config.APP_DEBUG.lower() == "false" else None,
            level="INFO",
            format='%(asctime)s - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s',
            force=True
        )

        self.logger = logging.getLogger()

    @staticmethod
    def get_logger(name: str):
        return logging.getLogger(name)


class I18n:
    def __init__(self, config: Config):
        i18n.load_path.append(os.path.dirname(os.path.abspath(__file__)) + '/../lang/')
        i18n.set('file_format', 'json')
        i18n.set('skip_locale_root_data', True)
        i18n.set('locale', config.APP_LOCALE)
        i18n.set('fallback', config.APP_FALLBACK_LOCALE)

    @staticmethod
    def get_locale() -> str:
        return i18n.get('locale')

    @staticmethod
    def set_locale(locale: str) -> None:
        i18n.set('locale', locale)

    @staticmethod
    def t(key: str) -> str:
        return i18n.t(key)
