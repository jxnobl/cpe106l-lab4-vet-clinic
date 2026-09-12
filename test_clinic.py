import unittest
from database import ClinicDatabase
from pet_factory import PetFactory, Dog, Cat

class TestClinicManagement(unittest.TestCase):
    def setUp(self):
        ClinicDatabase.reset_instance()
        self.db = ClinicDatabase.get_instance()

    def test_validate_singleton_instance(self):
        first_instance = ClinicDatabase.get_instance()
        second_instance = ClinicDatabase.get_instance()
        self.assertIs(first_instance, second_instance)

    def test_register_pet_owner(self):
        owner_id = self.db.register_owner("Juan Dela Cruz", "09170000000")
        owners = self.db.get_owners()
        
        self.assertIn(owner_id, owners)
        self.assertEqual(owners[owner_id]["name"], "Juan Dela Cruz")
        self.assertEqual(owners[owner_id]["contact"], "09170000000")

    def test_add_pet_record(self):
        owner_id = self.db.register_owner("Maria Dela Cruz", "09180000000")
        pet_id = self.db.generate_pet_id()
        
        pet = PetFactory.create_pet(pet_id, "Dog", "Bantay", owner_id)
        self.assertIsInstance(pet, Dog)
        
        self.db.add_pet(pet)
        pets = self.db.get_pets()
        
        self.assertIn(pet_id, pets)
        self.assertEqual(pets[pet_id].name, "Bantay")
        self.assertEqual(pets[pet_id].pet_type, "Dog")
        self.assertEqual(pets[pet_id].owner_id, owner_id)

    def test_schedule_appointment(self):
        apt_id = self.db.schedule_appointment("Bantay")
        appointments = self.db.get_appointments()
        
        self.assertIn(apt_id, appointments)
        self.assertEqual(appointments[apt_id]["pet_name"], "Bantay")
        self.assertEqual(appointments[apt_id]["status"], "Scheduled")

    def test_cancel_appointment(self):
        apt_id = self.db.schedule_appointment("Bantay")
        is_cancelled = self.db.cancel_appointment(apt_id)
        
        self.assertTrue(is_cancelled)
        appointments = self.db.get_appointments()
        self.assertEqual(appointments[apt_id]["status"], "Cancelled")

if __name__ == "__main__":
    unittest.main()