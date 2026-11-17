import logging
import json

class StructuredMessage:
    def __init__(self,message,/,**kwargs) -> None:
        self.message=message
        self.kwargs=kwargs

    def __str__(self) -> str:
        log_dict={"message":self.message}
        log_dict.update(self.kwargs)
        return json.dumps(log_dict)

structure=StructuredMessage

def process_order(order_id,customer_id,items,total_amount):
    logger=logging.getLogger('order_service ')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler=logging.StreamHandler()
        # This simple formatter ensures ONLY our JSON messaged is printed
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)

    logger.info(
        StructuredMessage("Order processed successfully",
        order_id=order_id,
        customer_id=customer_id,
        items=items,
        total_amount=total_amount))

# Let's process a sample order
process_order(1234567890,"C1234567890",["Item1","Item2","Item3"],100.00)