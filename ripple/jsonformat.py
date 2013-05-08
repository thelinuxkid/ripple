def drop(drops):
    """
    Converts a string to drops. A drop the smallest unit in the Ripple
    currency (0.000001 XRP)
    """
    if not drops.isdigit():
        raise ValueError(
            'Value must be a positive integer: {drops}'.format(
                drops=drops,
            )
        )
    # Python will automatically cast to long integer for any value not
    # in -sys.maxint - 1 <= x <= sys.maxint
    drops = int(drops)
    return drops
