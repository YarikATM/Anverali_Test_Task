from config.env_reader import config



LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(filename)s] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if config.DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'logfile': {
            'level': 'DEBUG' if config.DEBUG else 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "logs/logfile.log",
            'formatter': 'default',
            'maxBytes': 1024 * 1024 * 1024,
            'backupCount': 1
        },
    },
    'loggers': {
        "": {
            'handlers': ["console", "logfile"],
            'level': 'DEBUG' if config.DEBUG else 'INFO'
        }
    }
}