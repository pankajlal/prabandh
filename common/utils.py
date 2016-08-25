import logging
from django.conf import settings

logger = logging.getLogger(settings.APP_LOGGER)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('prabandh_info.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

