import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('myapp')
        self.logger.setLevel(logging.DEBUG)  # 로깅 레벨 설정
        handler = logging.FileHandler('myapp.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def error(self, message):
        self.logger.error(message)
