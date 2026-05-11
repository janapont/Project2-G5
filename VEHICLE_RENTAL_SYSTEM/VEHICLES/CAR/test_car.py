"""Unit tests for the Car class."""
import unittest
from datetime import date

from VEHICLES.CAR.car import Car
from VEHICLES.vehicle import Vehicle


def _years_ago(years):
    """Devuelve la fecha de hoy menos 'years' años (manejando 29 feb)."""
    today = date.today()
    try:
        return today.replace(year=today.year - years)
    except ValueError:
        return today.replace(year=today.year - years, day=28)


def _add_y(d, years):
    """Suma años a una fecha (manejando 29 feb)."""
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, day=28)


class TestCarITV(unittest.TestCase):
    """ITV de coche: cada 2 años del 4º al 10º, y luego cada año."""

    def test_itv_brand_new_car(self):
        matric = date.today()
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 4))

    def test_itv_2_years_old(self):
        matric = _years_ago(2)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 4))

    def test_itv_5_years_old_returns_year_6(self):
        matric = _years_ago(5)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 6))

    def test_itv_7_years_old_returns_year_8(self):
        matric = _years_ago(7)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 8))

    def test_itv_9_years_old_returns_year_10(self):
        matric = _years_ago(9)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 10))

    def test_itv_11_years_old_returns_year_12(self):
        matric = _years_ago(11)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 12))

    def test_itv_15_years_old_returns_year_16(self):
        matric = _years_ago(15)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
        self.assertEqual(car.calculate_ITV(), _add_y(matric, 16))

    def test_itv_always_in_future(self):
        for years in [0, 2, 4, 5, 6, 8, 10, 12, 20]:
            matric = _years_ago(years)
            car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 0)
            self.assertGreater(car.calculate_ITV(), date.today())


class TestCarMaintenance(unittest.TestCase):

    def test_maintenance_no_previous(self):
        matric = date(2020, 6, 15)
        car = Car("Seat", "red", "1234ABC", "Ibiza", matric, 10000)
        self.assertEqual(car.maintenance_schedule(), date(2021, 6, 15))

    def test_maintenance_with_previous(self):
        car = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 30000)
        car.register_maintenance(date(2024, 3, 10), 25000)
        self.assertEqual(car.maintenance_schedule(), date(2025, 3, 10))

    def test_maintenance_does_not_depend_on_mileage(self):
        car = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 30000)
        car.register_maintenance(date(2024, 3, 10), 25000)
        car.update_info(mileage=99999)
        self.assertEqual(car.maintenance_schedule(), date(2025, 3, 10))


class TestCarPolymorphism(unittest.TestCase):

    def test_car_is_instance_of_vehicle(self):
        car = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 0)
        self.assertIsInstance(car, Vehicle)

    def test_car_inherits_getters(self):
        car = Car("Seat", "red", "1234ABC", "Ibiza", date(2020, 1, 1), 5000)
        self.assertEqual(car.get_brand(), "Seat")
        self.assertEqual(car.get_mileage(), 5000)


if __name__ == "__main__":
    unittest.main()