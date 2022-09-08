class ErrorMessages:
    @staticmethod
    def stat_locked():
        raise PermissionError("cannot modify this object while .is_locked is set to a truthy value")
