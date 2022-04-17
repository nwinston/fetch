class TimestampException(Exception):
    """
    Exception class for timestamp errors.
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message