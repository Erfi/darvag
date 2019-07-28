

class APIException(Exception):
    """Base exception class for the project"""
    pass


class DatabaseException(APIException):
    """Database related exceptions"""
    pass


class DatabaseInsertException(DatabaseException):
    """Exception for inserting an entry"""
    pass
