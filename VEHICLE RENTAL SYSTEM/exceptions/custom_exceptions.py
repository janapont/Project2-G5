#vehicle exceptions
class InvalidBrandError(Exception):
    pass


class InvalidColorError(Exception):
    pass


class InvalidModelError(Exception):
    pass


class InvalidLicensePlateError(Exception):
    pass


class InvalidMatriculationDateError(Exception):
    pass


class InvalidMileageError(Exception):
    pass


class MileageCannotDecreaseError(Exception):
    pass

#users exceptions