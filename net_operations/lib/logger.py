import logging
from net_operations.lib.classes.NetFiles import NetFiles

fs = NetFiles()
logfile = fs.logfile
own_logger = logging.getLogger(__name__)
own_logger.setLevel(logging.INFO)
own_handler = logging.FileHandler(logfile, mode='a')
own_format = logging.Formatter("%(asctime)s >> %(levelname)s: %(message)s")
own_handler.setFormatter(own_format)
own_logger.addHandler(own_handler)
