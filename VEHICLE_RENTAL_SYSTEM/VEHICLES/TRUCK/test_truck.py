import unittest
from datetime import date

from VEHICLES.TRUCK.truck import Truck
from VEHICLES.vehicle import Vehicle


def _years_ago(years):
    today = date.today()
    try:
        return today.replace(year=today.year - years)
    except ValueError:
        return today.replace(year=today.year - years, day=28)


def _add_y(d, years):
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(year=d.year + years, day=28)


def _add_m(d, months):
    """Suma meses (mismo algoritmo que vehicle._add_months)."""
    total = d.month - 1 + months
    new_year = d.year + total // 12
    new_month = total % 12 + 1
    try:
        return d.replace(year=new_year, month=new_month)
    except ValueError:
        return d.replace(year=new_year, month=new_month, day=28)


class TestTruckITV(unittest.TestCase):
    """ITV de camión: cada año hasta el 10º, luego cada 6 meses."""

    def test_itv_brand_new(self):
        # Camión matriculado hoy -> ITV en 1 año
        matric = date.today()
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 0)
        self.assertEqual(truck.calculate_ITV(), _add_y(matric, 1))

    def test_itv_3_years_old_returns_year_4(self):
        matric = _years_ago(3)
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 0)
        self.assertEqual(truck.calculate_ITV(), _add_y(matric, 4))

    def test_itv_5_years_old_returns_year_6(self):
        matric = _years_ago(5)
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 0)
        self.assertEqual(truck.calculate_ITV(), _add_y(matric, 6))

    def test_itv_9_years_old_returns_year_10(self):
        matric = _years_ago(9)
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 0)
        self.assertEqual(truck.calculate_ITV(), _add_y(matric, 10))

    def test_itv_after_10_years_every_6_months(self):
        # Hace 11 años -> año 10 ya pasó -> debe sumar 6 meses hasta que sea futuro
        matric = _years_ago(11)
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 0)
        result = truck.calculate_ITV()
        # Debe ser una fecha futura, posterior a year_10
        self.assertGreater(result, date.today())
        self.assertGreater(result, _add_y(matric, 10))

    def test_itv_always_in_future(self):
        for years in [0, 1, 2, 5, 9, 10, 11, 12, 20]:
            matric = _years_ago(years)
            truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 0)
            self.assertGreater(truck.calculate_ITV(), date.today(),
                               f"Falla para camión de {years} años")


class TestTruckMaintenance(unittest.TestCase):
    """Mantenimiento de camión: cada 2 meses o cada 1000 km."""

    def test_maintenance_no_previous_low_km(self):
        # Sin mantenimiento previo, pocos km -> 2 meses desde matriculación
        matric = date(2020, 6, 15)
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 500)
        self.assertEqual(truck.maintenance_schedule(), _add_m(matric, 2))

    def test_maintenance_no_previous_high_km(self):
        # Sin mantenimiento previo y >= 1000 km -> hoy
        matric = date(2020, 6, 15)
        truck = Truck("Volvo", "white", "1234ABC", "FH", matric, 2000)
        self.assertEqual(truck.maintenance_schedule(), date.today())

    def test_maintenance_with_previous_low_km(self):
        # Con mantenimiento previo, pocos km extra -> 2 meses desde último
        truck = Truck("Volvo", "white", "1234ABC", "FH", date(2020, 1, 1), 5500)
        truck.register_maintenance(date(2024, 3, 10), 5000)
        # 500 km extra desde el último -> por tiempo
        self.assertEqual(truck.maintenance_schedule(), date(2024, 5, 10))

    def test_maintenance_with_previous_high_km(self):
        # Con mantenimiento previo y >= 1000 km extra -> hoy
        truck = Truck("Volvo", "white", "1234ABC", "FH", date(2020, 1, 1), 6500)
        truck.register_maintenance(date(2024, 3, 10), 5000)
        # 1500 km extra desde el último -> por km
        self.assertEqual(truck.maintenance_schedule(), date.today())

    def test_maintenance_exactly_1000_km(self):
        truck = Truck("Volvo", "white", "1234ABC", "FH", date(2020, 1, 1), 6000)
        truck.register_maintenance(date(2024, 3, 10), 5000)
        self.assertEqual(truck.maintenance_schedule(), date.today())


class TestTruckPolymorphism(unittest.TestCase):

    def test_truck_is_instance_of_vehicle(self):
        truck = Truck("Volvo", "white", "1234ABC", "FH", date(2020, 1, 1), 0)
        self.assertIsInstance(truck, Vehicle)

    def test_truck_inherits_getters(self):
        truck = Truck("Volvo", "white", "1234ABC", "FH", date(2020, 1, 1), 5000)
        self.assertEqual(truck.get_brand(), "Volvo")
        self.assertEqual(truck.get_mileage(), 5000)


if __name__ == "__main__":
    unittest.main()