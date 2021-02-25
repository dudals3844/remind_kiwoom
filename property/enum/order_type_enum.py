from enum import Enum


class OrderTypeEnum(Enum):
    MESU = 1
    MEDO = 2
    CANCEL_MESU = 3
    CANCEL_MEDO = 4
    MODIFY_MESU = 5
    MODIFY_MEDO = 6
