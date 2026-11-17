import logging
import json
import os # To help with the log file

class StructuredMessage:
    def __init__(self, message, /, **kwargs):
        self.message = message
        self.kwargs = kwargs


    def __str__(self):
        log_dict = {'message': self.message}
        log_dict.update(self.kwargs)
        return json.dumps(log_dict)
    
structure=StructuredMessage

def update_inventory(item_id,quantity):
    logger=logging.getLogger('inventory_service')
    logger.setLevel(logging.INFO) # Set the lowest level of logging

    if not logger.handlers:
        #Handler 1: Console Handler show INFO and above
        console_handler=logging.StreamHandler() 
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(console_handler)

        #Handler 2: File Handler ONLY show WARNING and above
        file_handler=logging.FileHandler('inventory.log')
        file_handler.setLevel(logging.WARNING) # Higher threshold for the file
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s -%(message)s'))
        
        logger.addHandler(file_handler)
        logger.info(structure('Checking inventory for item  ', item_id=item_id))
    if quantity < 10:
            logger.warning(structure('Inventory low', item_id=item_id,
             stock_level=quantity))
    if quantity == 0:
            logger.error(structure('Inventory out of stock', item_id=item_id))

# Let's run a few updates
if os.path.exists('inventory.log'):
    os.remove('inventory.log')


update_inventory('ITEM-A', 50)
update_inventory('ITEM-B', 20)
update_inventory('ITEM-C', 0)

