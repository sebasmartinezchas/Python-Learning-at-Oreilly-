import logging
import json


class StructuredMessage:
    def __init__(self,message,/,**kwargs) -> None:
        self.message=message
        self.kwargs=kwargs

    def __str__(self) -> str:
        log_dict={"message": self.message}
        log_dict.update(self.kwargs)
        return json.dumps(log_dict)

structure=StructuredMessage


def log_login_attemp(username,is_successful,is_locked):

    """
    Process a usar login attemp with comprehnsive structured logging.
    Requirements:
    1 . Configure a named logger called 'auth_service'
    2 . User the 'structure' helper to produce pure JSON output
    3 . Log successful logins as INFO with the username
    4 . Log failded logins as WARNING with the username
    5 . Log attempts on locked accounts as ERROR with the username
    # Your implementation here
    """
    logger=logging.getLogger('auth_service')
    logger.setLevel(logging.INFO) # Set the lowest level of logging


    if not logger.handlers:
        # Handler 1: Console handler show INFO and above
        console_handler=logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(console_handler)

        # Handler 2: File handler ONLY show warning and above
        file_handler=logging.FileHandler('service_log')
        file_handler.setLevel(logging.WARNING) # Higher threshold for the file
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s -%(message)s'))
        logger.addHandler(file_handler)

    if not is_successful:
        logger.warning(structure("Failed login attempt for user:", username=username))

    if is_locked:
        logger.error(structure("Login attempt on locked account:",username=username))

    if is_successful:
        logger.info(structure('Successful login',username=username))

# Test cases:
log_login_attemp("alice",is_successful=True,is_locked=False)
log_login_attemp("bob",is_successful=False,is_locked=False)
log_login_attemp("charlie",is_successful=False,is_locked=True)
