from abc import ABC, abstractmethod
from decimal import Decimal

class AbstractExchange(ABC):
    def __init__(self, request_timeout: int = 20, request_delay: int = 2) -> None:
        super(AbstractExchange, self).__init__()
        self.request_timeout = request_timeout
        self.request_delay = request_delay

    @classmethod
    @abstractmethod
    def set_order(cls, currency: str, amount: Decimal) -> dict:
        pass

    @classmethod
    @abstractmethod
    def buy_from_exchange(cls, currency: str, amount: Decimal) -> dict:
        pass

    @classmethod
    @abstractmethod
    def sell_to_exchange(cls, currency_code: str, amount: Decimal) -> dict:
        pass
