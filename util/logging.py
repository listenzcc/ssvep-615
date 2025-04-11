from loguru import logger

logger.add('logs/debug.log', level='DEBUG',
           rotation='1 MB', retention='10 days')
