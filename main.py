from custom_logging.logging import get_logger


logger = get_logger('graphics')
logger2 = get_logger('sound')

if __name__ == "__main__":
    logger.info('Hello World!')
    logger2.info('Hello AGAIN!')
