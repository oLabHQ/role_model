
def join_and(iterable, plural=False):
    """
    Return a comma separated string for items in iterable, where the last comma
    is replaced by "and a" or "and", depending on `plural` argument.
    """

    # Remove any empty strings.
    values = list(filter(None, [str(value) for value in iterable]))

    if not values:
        return ""

    value = values.pop()

    if plural:
        return " and ".join(filter(None, [", ".join(values), value]))

    return " and a ".join(filter(None, [", a ".join(values), value]))


def join_comma(iterable):
    """
    Return a comma separated string for items in iterable.
    """

    # Remove any empty strings.
    values = list(filter(None, [str(value) for value in iterable]))

    if not values:
        return ""

    return ", ".join(values)
