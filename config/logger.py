import logging


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        logger = logging.getLogger("uvicorn")
        logger.setLevel(logging.INFO)

        log_file = "log/logs.log"
        file_handler = logging.FileHandler(log_file)

        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger
