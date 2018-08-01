from enum import Enum


class AutoName(Enum):
    """
    Enum generates integer values. Use this AutoName inheriting Enum to
    have `enum.auto()` use string values.
    """
    def _generate_next_value_(name, start, count, last_values):
        return name
