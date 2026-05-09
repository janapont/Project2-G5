import unittest
from datetime import date

from VEHICLES.MOTORBIKE.motorbike import Motorbike
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


class TestMotorbikeITV(unittest.TestCase):
    """ITV de moto: año 4 y luego cada 2 años."""

    def test_itv_brand_new(self):
        # Moto matriculada hoy -> ITV en 4 años
        matric = date.today()
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 0)
        self.assertEqual(moto.calculate_ITV(), _add_y(matric, 4))

    def test_itv_2_years_old(self):
        matric = _years_ago(2)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 0)
        self.assertEqual(moto.calculate_ITV(), _add_y(matric, 4))

    def test_itv_5_years_old_returns_year_6(self):
        # Año 4 ya pasó -> próxima año 6
        matric = _years_ago(5)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 0)
        self.assertEqual(moto.calculate_ITV(), _add_y(matric, 6))

    def test_itv_7_years_old_returns_year_8(self):
        matric = _years_ago(7)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 0)
        self.assertEqual(moto.calculate_ITV(), _add_y(matric, 8))

    def test_itv_10_years_old_returns_year_12(self):
        # Año 4, 6, 8, 10 ya pasaron -> próxima año 12
        matric = _years_ago(10)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 0)
        self.assertEqual(moto.calculate_ITV(), _add_y(matric, 12))

    def test_itv_always_in_future(self):
        for years in [0, 2, 4, 5, 6, 8, 10, 12, 20]:
            matric = _years_ago(years)
            moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 0)
            self.assertGreater(moto.calculate_ITV(), date.today(),
                               f"Falla para moto de {years} años")


class TestMotorbikeMaintenance(unittest.TestCase):
    """Mantenimiento de moto: cada año o cada 1000 km desde el último."""

    def test_maintenance_no_previous_low_km(self):
        # Sin mantenimiento previo, pocos km -> 1 año desde matriculación
        matric = date(2020, 6, 15)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 500)
        self.assertEqual(moto.maintenance_schedule(), date(2021, 6, 15))

    def test_maintenance_no_previous_high_km(self):
        # Sin mantenimiento previo y >= 1000 km -> hoy (toca mantenimiento)
        matric = date(2020, 6, 15)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 1500)
        self.assertEqual(moto.maintenance_schedule(), date.today())

    def test_maintenance_no_previous_exactly_1000_km(self):
        matric = date(2020, 6, 15)
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", matric, 1000)
        self.assertEqual(moto.maintenance_schedule(), date.today())

    def test_maintenance_with_previous_low_km(self):
        # Con mantenimiento previo, pocos km extra -> 1 año desde último
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", date(2020, 1, 1), 5500)
        moto.register_maintenance(date(2024, 3, 10), 5000)
        # Solo 500 km extra desde el último mantenimiento -> por tiempo
        self.assertEqual(moto.maintenance_schedule(), date(2025, 3, 10))

    def test_maintenance_with_previous_high_km(self):
        # Con mantenimiento previo y >= 1000 km extra -> hoy
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", date(2020, 1, 1), 6500)
        moto.register_maintenance(date(2024, 3, 10), 5000)
        # 1500 km extra desde el último -> por km
        self.assertEqual(moto.maintenance_schedule(), date.today())


class TestMotorbikePolymorphism(unittest.TestCase):

    def test_motorbike_is_instance_of_vehicle(self):
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", date(2020, 1, 1), 0)
        self.assertIsInstance(moto, Vehicle)

    def test_motorbike_inherits_getters(self):
        moto = Motorbike("Honda", "black", "1234ABC", "Forza", date(2020, 1, 1), 5000)
        self.assertEqual(moto.get_brand(), "Honda")
        self.assertEqual(moto.get_mileage(), 5000)


if __name__ == "__main__":
    unittest.main()