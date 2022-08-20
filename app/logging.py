import logging

LOGGING_LEVEL_COLOR_MAP = {
    logging.DEBUG: '34',
    logging.INFO: '32',
    logging.WARNING: '33',
    logging.ERROR: '31',
    logging.CRITICAL: '41',
}

for level, color in LOGGING_LEVEL_COLOR_MAP.items():
    logging.addLevelName(level, "\033[1;{}m{}\033[1;0m".format(color, logging.getLevelName(level)))


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename='./server.log')
formatter = logging.Formatter('[%(levelname)s][%(asctime)s] - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)
