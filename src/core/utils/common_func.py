from enum import Enum


def get_enum_values(enum: Enum):
    return [e.value for e in enum]