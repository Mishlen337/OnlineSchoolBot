
class ConnectionError(Exception):
    pass


class UniqueError(Exception):
    pass


class OrderCourseExists(UniqueError):
    pass


class StudentExists(UnicodeError):
    pass


class NoSuchCoursePackage(Exception):
    pass
