import logging, os


# class Logger:
#     def __init__(self, name):
#         self.name = name
#
#     def log(self, logDir):
#         # __name__ = name
#         logger = logging.getLogger(self.name)
#         logger.setLevel(logging.DEBUG)
#
#         if not os.path.exists(logDir):
#             os.mkdir(logDir)
#         # create a file handler
#         handler = logging.FileHandler(logDir + "/log.log")
#         handler.setLevel(logging.DEBUG)
#
#         # create a logging format
#         formatter = logging.Formatter('[' + '%(asctime)s' + ']' + ' - %(name)s - %(levelname)s - %(message)s')
#         handler.setFormatter(formatter)
#
#         consoleHandler = logging.StreamHandler()
#         consoleHandler.setFormatter(formatter)
#
#         # add the handlers to the logger
#         logger.addHandler(handler)
#         logger.addHandler(consoleHandler)
#         return logger


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=SingletonType):
	_logger = None

	def __init__(self, name, logDir):
		self._logger = logging.getLogger(name)
		self._logger.setLevel(logging.DEBUG)

		if not os.path.isdir(logDir):
			os.mkdir(logDir)

		handler = logging.FileHandler(logDir + "/log.log")
		handler.setLevel(logging.DEBUG)

		formatter = logging.Formatter('[' + '%(asctime)s' + ']' + ' - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)

		consoleHandler = logging.StreamHandler()
		consoleHandler.setFormatter(formatter)

		self._logger.addHandler(handler)
		self._logger.addHandler(consoleHandler)

	def get_logger(self):
		return self._logger
