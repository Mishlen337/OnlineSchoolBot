
class ConnectionError(Exception):
    pass


class UniqueError(Exception):
    pass


class OrderCourseExists(UniqueError):
    pass


class StudentExists(UniqueError):
    pass


class NoSuchCoursePackage(Exception):
    pass


class NoSuchTutor(Exception):
    pass


class AccessError(Exception):
    pass


class DoneHomeworkExists(UniqueError):
    pass


class NoSuchLessonOrNoAssistants(Exception):
    pass


class NoSuchWebinarOrNoAssistants(Exception):
    pass


class DeadlineError(Exception):
    pass


class GroupSingUpError(UniqueError):
    pass


class NoSuchGroupLessonOrNoAssistants(Exception):
    pass
