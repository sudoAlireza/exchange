from abc import ABC, abstractmethod
from decimal import Decimal

class AbstractExchange(ABC):
    def __init__(self, request_timeout: int = 20, request_delay: int = 2) -> None:
        super(AbstractExchange, self).__init__()
        self.request_timeout = request_timeout
        self.request_delay = request_delay

    @abstractmethod
    def set_order(currnecy: str, amount: Decimal):
        pass

    @abstractmethod
    def buy_from_exchange(currnecy: str, amount: Decimal):
        pass

    @abstractmethod
    def sell_to_exchange(cls, currency_code, amount) -> dict:
        pass
