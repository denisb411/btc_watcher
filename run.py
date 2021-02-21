import signal
import time
import traceback

from utils.btc_utils import PriceWatcher
from utils.email_utils import EmailSender
from utils.config_utils import config
from utils.logging_utils import create_default_logger

logger = create_default_logger(__file__)

class ServiceExit(Exception):
    pass

def service_shutdown(signum, frame):
    logger.debug('Caught signal %d' % signum)
    raise ServiceExit

if __name__ == "__main__":
    signal.signal(signal.SIGINT, service_shutdown)
    signal.signal(signal.SIGTERM, service_shutdown)

    email_sender = EmailSender(config['email_login'], config['email_password'])

    try:
        price_watcher = PriceWatcher(email_sender, 
                                    currency_code=config['currency_code'],
                                    warn_threshold_above=config['warn_threshold_above'],
                                    warn_threshold_below=config['warn_threshold_below'],
                                    sleep_time_seconds=config['sleep_time_seconds'])

        while True:
            time.sleep(0.5)

    except ServiceExit:
        price_watcher.stop()

    except Exception as err:
        logger.critical(traceback.format_exc() + '\n' + str(err))