"""Exceptions for use with prjct."""

class PrjctError(Exception):
    """Base class for prjct errors to be derived from."""

    pass

class ConfigKeyMissingError(PrjctError, KeyError):
    """The desired key is not in the configuration."""

    pass
