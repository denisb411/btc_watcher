import requests
import traceback
import threading
import datetime
import time

from utils.logging_utils import create_default_logger

logger = create_default_logger(__file__)

def get_last_price(currency_code='BRL'):

    try:
        response = requests.get('https://blockchain.info/ticker')
    except Exception as err:
        logger.critical(traceback.format_exc())
        raise err

    if response.status_code != 200:
        logger.error(f"GET on https://blockchain.info/ticker returned status_code = {response.status_code}")

    data = response.json()
    currency_btc = data.get(currency_code, None)
    logger.debug(currency_btc)

    if currency_btc is None:
        raise ValueError("Invalid currency_code")

    return currency_btc['last']

class PriceWatcher(threading.Thread):
    def __init__(
        self, 
        email_sender,
        name='price watcher', 
        currency_code='BRL',
        warn_threshold_above=350000,
        warn_threshold_below=290000,
        sleep_time_seconds=1,
        time_delta_between_sent_emails=datetime.timedelta(minutes=2)
    ):
        super(PriceWatcher, self).__init__()

        self.__running = threading.Event ()   
        self.__running.set ()

        self.name = name
        self.currency_code = currency_code
        self.sleep_time_seconds = sleep_time_seconds
        self.email_sender = email_sender

        self.warn_threshold_below = warn_threshold_below
        self.warn_threshold_above = warn_threshold_above

        self.time_delta_between_sent_emails = time_delta_between_sent_emails
        self.email_sent_datetime = None

        self.start()

        logger.debug("Price watcher started")

    def __send_email_price(self, current_price):
        self.email_sender.send_to_myself('[BTCPriceWatcher] BTC price below set threshold', 
                                         (
                                            f'Above threshold: {self.warn_threshold_above}\n'
                                            f'Below threshold: {self.warn_threshold_below}\n'
                                            f'Current price: {current_price}\n'
                                            f'Currency: {self.currency_code}'
                                         ))
        self.email_sent_datetime = datetime.datetime.now()

    def run(self):
        while self.__running.is_set():

            last_btc_price = get_last_price(currency_code=self.currency_code)

            if last_btc_price < self.warn_threshold_below \
                or last_btc_price > self.warn_threshold_above:

                if self.email_sent_datetime is None:
                    self.__send_email_price(last_btc_price)

                else:
                    if self.email_sent_datetime + self.time_delta_between_sent_emails < datetime.datetime.now():
                        self.__send_email_price(last_btc_price)

            logger.info(f"Done checking. Current BTC price: {last_btc_price}")

            time.sleep(self.sleep_time_seconds)

        logger.info('PriceWatcher stopped' % self.ident)

    def stop(self):
        self.__running.clear()
        self.join()