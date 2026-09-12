import threading
import itertools

class ClinicDatabase:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ClinicDatabase, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._owners = {}
        self._pets = {}
        self._appointments = {}
        self._pet_counter = itertools.count(1)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None

    def register_owner(self, owner_id, name, contact):
        clean_id = str(owner_id).strip()
        clean_name = str(name).strip()
        clean_contact = str(contact).strip()

        if not clean_id or not clean_name or not clean_contact:
            raise ValueError("Owner ID, Name, and Contact Number cannot be empty.")

        if clean_id in self._owners:
            raise ValueError(f"Owner ID '{clean_id}' already exists.")

        self._owners[clean_id] = {
            "owner_id": clean_id,
            "name": clean_name,
            "contact": clean_contact
        }
        return self._owners[clean_id]

    def get_owners(self):
        return self._owners

    def generate_pet_id(self):
        return f"PET-{next(self._pet_counter):04d}"

    def add_pet(self, pet):
        clean_owner_id = str(pet.owner_id).strip()
        if clean_owner_id not in self._owners:
            raise KeyError(f"Cannot add pet: Owner ID '{clean_owner_id}' does not exist.")
        self._pets[pet.pet_id] = pet

    def get_pets(self):
        return self._pets

    def schedule_appointment(self, appointment_id, pet_name):
        clean_apt_id = str(appointment_id).strip()
        clean_pet_name = str(pet_name).strip()

        if not clean_apt_id or not clean_pet_name:
            raise ValueError("Appointment ID and Pet Name cannot be empty.")

        if clean_apt_id in self._appointments:
            raise ValueError(f"Appointment ID '{clean_apt_id}' already exists.")

        self._appointments[clean_apt_id] = {
            "appointment_id": clean_apt_id,
            "pet_name": clean_pet_name,
            "status": "Scheduled"
        }
        return self._appointments[clean_apt_id]

    def update_appointment_status(self, appointment_id, status):
        clean_apt_id = str(appointment_id).strip()
        valid_statuses = {"Scheduled", "Completed", "Cancelled"}
        formatted_status = str(status).strip().capitalize()

        if formatted_status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Allowed values: {', '.join(sorted(valid_statuses))}")

        if clean_apt_id in self._appointments:
            self._appointments[clean_apt_id]["status"] = formatted_status
            return True
        return False

    def cancel_appointment(self, appointment_id):
        return self.update_appointment_status(appointment_id, "Cancelled")

    def get_appointments(self):
        return self._appointments

    def clear(self):
        self._owners.clear()
        self._pets.clear()
        self._appointments.clear()
        self._pet_counter = itertools.count(1)