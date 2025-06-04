from datetime import timedelta
from decimal import Decimal
from typing import Final

DEFAULT_BALANCE: Final = Decimal("5000.00")
# TODO: change to normal value
MONTH_DELTA: Final = timedelta(minutes=1)
# MONTH_DELTA: Final = timedelta(days=30)
WITHDRAWAL: Final = Decimal("500")

__all__ = ["DEFAULT_BALANCE", "MONTH_DELTA", "WITHDRAWAL"]
