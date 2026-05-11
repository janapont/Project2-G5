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
class InvalidDateOfBirth(Exception):
    pass

class InvalidName(Exception):
    pass

class VehicleAlreadyRegistered(Exception):
    pass

class VehicleNotFound(Exception):
    pass

class InvalidRole(Exception):
    pass

#rental exceptions
class InvalidRentalPeriod(Exception):
    pass

class InvalidKms(Exception):
    pass

class InvalidAssurance(Exception):
    pass

class RentalNotActive(Exception):
    pass

class KmsExceeded(Exception):
    pass

#shop management exceptions
class ClientAlreadyExists(Exception):
    pass

class ClientNotFound(Exception):
    pass

class WorkerAlreadyExists(Exception):
    pass

class WorkerNotFound(Exception):
    pass

class RentalAlreadyExists(Exception):
    pass

class RentalNotFound(Exception):
    pass