import unittest
from database import ClinicDatabase
from pet_factory import PetFactory, Dog, Cat, Bird, Rabbit

class TestClinicManagement(unittest.TestCase):
    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase.get_instance()

    def test_singleton_instance(self):
        second_reference = ClinicDatabase.get_instance()
        self.assertIs(self.db, second_reference)

    def test_register_pet_owner(self):
        self.db.register_owner("O-100", "Carlos", "09171234567")
        owners = self.db.get_owners()
        self.assertIn("O-100", owners)
        self.assertEqual(owners["O-100"]["name"], "Carlos")
        self.assertEqual(owners["O-100"]["contact"], "09171234567")

    def test_add_pet_record(self):
        self.db.register_owner("O-100", "Carlos", "09171234567")
        dog = PetFactory.create_pet("Dog", "Browny", "O-100")
        self.assertIsInstance(dog, Dog)
        self.assertEqual(dog.speak(), "Woof!")
        
        self.db.add_pet(dog)
        pets = self.db.get_pets()
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].name, "Browny")
        self.assertEqual(pets[0].owner_id, "O-100")

    def test_schedule_appointment(self):
        self.db.schedule_appointment("APT-01", "Browny")
        appointments = self.db.get_appointments()
        self.assertIn("APT-01", appointments)
        self.assertEqual(appointments["APT-01"]["pet_name"], "Browny")
        self.assertEqual(appointments["APT-01"]["status"], "Scheduled")

    def test_cancel_appointment(self):
        self.db.schedule_appointment("APT-02", "Browny")
        status_updated = self.db.cancel_appointment("APT-02")
        self.assertTrue(status_updated)
        appointments = self.db.get_appointments()
        self.assertEqual(appointments["APT-02"]["status"], "Cancelled")

if __name__ == "__main__":
    unittest.main()