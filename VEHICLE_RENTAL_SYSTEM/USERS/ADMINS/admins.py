from USERS.users import User
from custom_exceptions import InvalidRole


ROLES = ["mechanic", "rental manager", "administrator"]

class Admin(User):
    def __init__(self, name, date_of_birth, role):
        super().__init__(name, date_of_birth)
        self.validate_role(role)
        self.__role = role

    def validate_role(self, role):
        if role not in ROLES:
            raise InvalidRole(f"Role must be one of: {ROLES}")

    def get_type(self):
        return "admin"

    def get_role(self):
        return self.__role

    def update_role(self, role):
        self.validate_role(role)
        self.__role = role

    def to_csv_line(self):
        return (
            f"{self.get_id()},"
            f"{self.get_name()},"
            f"{self.get_date_of_birth().isoformat()},"
            f"{self.get_role()}"
        )
    

def admin_from_csv_line(line):
    from datetime import date
    parts = line.strip().split(",")

    name = parts[0]
    date_of_birth = date.fromisoformat(parts[1])
    user_id = parts[2]
    role = parts[3]

    return Admin(name, date_of_birth, user_id, role)