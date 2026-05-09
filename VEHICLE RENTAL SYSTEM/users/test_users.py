from unittest import TestCase
from datetime import date
from users import User
from custom_exceptions import InvalidName, InvalidDateOfBirth

class ConcreteUser(User):    #  PORQUE LA CLASS USERS ES ABSTRACT Y NO PODEMOS CREAR OBJETOS
    def get_type(self):
        return "concrete"

class TestUser(TestCase):
    def test_create_user(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        self.assertEqual(user.get_name(), "Ana Garcia")
        self.assertEqual(user.get_date_of_birth(), date(2007, 6, 20))
        self.assertIsNotNone(user.get_id())
        self.assertIsInstance(user.get_id(), int)

    def test_ids_unique(self):
        user1 = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user2 = ConcreteUser("Sofia Perez", date(1985, 3, 20))
        self.assertNotEqual(user1.get_id(), user2.get_id())
    
    def test_id_increment(self):
        user1 = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user2 = ConcreteUser("Sofia Perez", date(1985, 3, 20))
        self.assertEqual(user1.get_id() + 1, user2.get_id())

    def test_invalid_name_string(self):
        with self.assertRaises(InvalidName):
            ConcreteUser(123, date(2007, 6, 20))

    def test_invalid_name_empty(self):
        with self.assertRaises(InvalidName):
            ConcreteUser("   ", date(2007, 6, 20))

    def test_invalid_date_object(self):
        with self.assertRaises(InvalidDateOfBirth):
            ConcreteUser("Ana Garcia", "2007-06-20")

    def test_invalid_date_future(self):
        with self.assertRaises(InvalidDateOfBirth):
            ConcreteUser("Ana Garcia", date(2100, 1, 1))

    def test_get_age(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        today = date.today()
        expected_age = today.year - 2007
        if today.month < 6:
            expected_age -= 1
        elif today.month == 6:
            if today.day < 20:
                expected_age -= 1
        self.assertEqual(user.get_age(), expected_age)
    
    def test_update_name(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user.update_name("Ana Gomez")
        self.assertEqual(user.get_name(), "Ana Gomez")

    def test_update_date_of_birth(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        user.update_date_of_birth(date(2010, 7, 3))
        self.assertEqual(user.get_date_of_birth(), date(2010, 7, 3))
    
    def test_get_type(self):
        user = ConcreteUser("Ana Garcia", date(2007, 6, 20))
        self.assertEqual(user.get_type(), "concrete")