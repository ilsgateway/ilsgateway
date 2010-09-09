import logging.handlers

def init_file_logging(log_file, log_size, log_backups, log_level, log_format):
    """
    Initializes logging for the Django side of RapidSMS, using a little hack
    to ensure that it only gets initialized once.  Derived from:

    http://stackoverflow.com/questions/342434/python-logging-in-django

    This is necessary if the logging is initialized in settings.py, but it
    may not be if it's initialized through project.wsgi.  Logging can't be
    initialized in the settings file because the route process also uses
    settings and sets up its own logging in the management command.
    """
    root_logger = logging.getLogger()
    if getattr(root_logger, 'django_log_init_done', False):
        return
    root_logger.django_log_init_done = True
    file = logging.handlers.RotatingFileHandler(log_file,
                                                maxBytes=log_size,
                                                backupCount=log_backups)
    root_logger.setLevel(getattr(logging, log_level))
    file.setLevel(getattr(logging, log_level))
    file.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(file)
    logger = logging.getLogger(__name__)
    logger.info('logger initialized')