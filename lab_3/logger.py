import logging 
from logging import StreamHandler, FileHandler, Formatter
import sys

class CustomFormatter(Formatter):
    grey = '\033[37m'
    green = '\033[32m'
    yellow = '\033[33m'
    red = '\033[31m'
    bold_red = '\033[31m\033[1m\033[6m'
    reset = '\033[0m'

    FORMATS = {
        logging.DEBUG: '[%(asctime)s]:[' + grey + '%(levelname)s' + reset + ']:['+yellow+'%(name)s'+reset+']:%(message)s',
        logging.INFO: '[%(asctime)s]:[' + green + '%(levelname)s' + reset + ']:['+yellow+'%(name)s'+reset+']:%(message)s',
        logging.WARNING: '[%(asctime)s]:[' + yellow + '%(levelname)s' + reset + ']:['+yellow+'%(name)s'+reset+']:%(message)s',
        logging.ERROR: '[%(asctime)s]:[' + red + '%(levelname)s' + reset + ']:['+yellow+'%(name)s'+reset+']:%(message)s',
        logging.CRITICAL: '[%(asctime)s]:[' + bold_red + '%(levelname)s' + reset + ']:['+yellow+'%(name)s'+reset+']:%(message)s'
    }

    def format(self, record):
        import platform
        if platform.system() == 'Windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

if __name__ == '__main__':
    # инициализация журналирования
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.INFO)

    # добавление обработчиков
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    file_path = './action_log.txt'
    log_handler = FileHandler(file_path,mode='w',encoding='utf-8')
    log_handler.setFormatter(Formatter(fmt='[%(asctime)s]:%(levelname)s:%(name)s:%(message)s'))
    logger.addHandler(log_handler)
    
    # пример использования 
    logger.info('Информационное сообщение')
    logger.warning('Предупреждающее сообщение')
    logger.error('Сообщение об ошибке')