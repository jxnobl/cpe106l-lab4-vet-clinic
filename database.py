import threading
import itertools


class ClinicCollection(dict):
    def __getitem__(self, key):
        if isinstance(key, int):
            values = list(self.values())
            if 0 <= key < len(values):
                return values[key]
            raise IndexError("list index out of range")
        return super().__getitem__(key)


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
        self._owners = ClinicCollection()
        self._pets = ClinicCollection()
        self._appointments = ClinicCollection()
        self._owner_counter = itertools.count(1)
        self._pet_counter = itertools.count(1)
        self._apt_counter = itertools.count(1)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None

    def generate_owner_id(self):
        return f"OWN-{next(self._owner_counter):04d}"

    def generate_pet_id(self):
        return f"PET-{next(self._pet_counter):04d}"

    def generate_appointment_id(self):
        return f"APT-{next(self._apt_counter):04d}"

    def register_owner(self, owner_id_or_name, name=None, contact=None):
        if contact is None:
            if name is None:
                raise TypeError("register_owner requires either (name, contact) or (owner_id, name, contact)")
            name, contact = owner_id_or_name, name
            owner_id = self.generate_owner_id()
        else:
            owner_id = str(owner_id_or_name).strip()
            if not owner_id:
                raise ValueError("Owner ID cannot be empty.")

        clean_name = str(name).strip()
        clean_contact = str(contact).strip()

        if not clean_name or not clean_contact:
            raise ValueError("Owner Name and Contact Number cannot be empty.")

        if contact is None:
            owner_id = self.generate_owner_id()

        self._owners[owner_id] = {
            "owner_id": owner_id,
            "name": clean_name,
            "contact": clean_contact
        }
        return owner_id

    def get_owners(self):
        return self._owners

    def add_pet(self, pet):
        clean_owner_id = str(pet.owner_id).strip()
        if clean_owner_id not in self._owners:
            raise KeyError(f"Cannot add pet: Owner ID '{clean_owner_id}' does not exist.")
        self._pets[pet.pet_id] = pet

    def get_pets(self):
        return self._pets

    def schedule_appointment(self, appointment_id_or_pet_name, pet_name=None):
        if pet_name is None:
            clean_pet_name = str(appointment_id_or_pet_name).strip()
            if not clean_pet_name:
                raise ValueError("Pet Name cannot be empty.")
            apt_id = self.generate_appointment_id()
        else:
            apt_id = str(appointment_id_or_pet_name).strip()
            if not apt_id:
                raise ValueError("Appointment ID cannot be empty.")
            clean_pet_name = str(pet_name).strip()
            if not clean_pet_name:
                raise ValueError("Pet Name cannot be empty.")

        self._appointments[apt_id] = {
            "appointment_id": apt_id,
            "pet_name": clean_pet_name,
            "status": "Scheduled"
        }
        return apt_id

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
        self._owner_counter = itertools.count(1)
        self._pet_counter = itertools.count(1)
        self._apt_counter = itertools.count(1)