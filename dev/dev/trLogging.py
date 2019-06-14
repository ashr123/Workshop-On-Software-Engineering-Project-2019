is_logging = False


if is_logging
import logging

log_setup = logging.getLogger('event log')
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
fileHandler = logging.FileHandler('event.log', mode='a')
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
log_setup.setLevel(logging.INFO)
log_setup.addHandler(fileHandler)
log_setup.addHandler(streamHandler)
log_setup1 = logging.getLogger('error log')
fileHandler1 = logging.FileHandler('error.log', mode='a')
fileHandler1.setFormatter(formatter)
streamHandler1 = logging.StreamHandler()
streamHandler1.setFormatter(formatter)
log_setup1.setLevel(logging.ERROR)
log_setup1.addHandler(fileHandler1)
log_setup1.addHandler(streamHandler1)
logev = logging.getLogger('event log')
loger = logging.getLogger('error log')