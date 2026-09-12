import threading
import itertools
import json
import os
from pet_factory import PetFactory

class ClinicDatabase:
    _instance = None
    _lock = threading.Lock()
    _storage_file = "clinic_data.json"

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
        self._owner_counter = itertools.count(1)
        self._pet_counter = itertools.count(1)
        self._apt_counter = itertools.count(1)
        self._load_from_disk()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None

    def _save_to_disk(self):
        serialized_pets = {}
        for pid, pet in self._pets.items():
            serialized_pets[pid] = {
                "pet_id": pet.pet_id,
                "pet_type": pet.pet_type,
                "name": pet.name,
                "owner_id": pet.owner_id
            }

        data = {
            "owners": self._owners,
            "pets": serialized_pets,
            "appointments": self._appointments
        }
        with open(self._storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def _load_from_disk(self):
        if not os.path.exists(self._storage_file):
            return

        try:
            with open(self._storage_file, "r") as f:
                data = json.load(f)

            self._owners = data.get("owners", {})
            self._appointments = data.get("appointments", {})

            # Reconstruct pet objects using PetFactory
            raw_pets = data.get("pets", {})
            for pid, pinfo in raw_pets.items():
                pet_obj = PetFactory.create_pet(
                    pinfo["pet_id"],
                    pinfo["pet_type"],
                    pinfo["name"],
                    pinfo["owner_id"]
                )
                self._pets[pid] = pet_obj

            # Re-sync auto-increment counters to prevent ID collisions
            self._sync_counters()

        except (json.JSONDecodeError, KeyError):
            pass

    def _sync_counters(self):
        owner_ids = [int(k.split("-")[1]) for k in self._owners.keys() if k.startswith("OWN-")]
        max_owner = max(owner_ids, default=0)
        self._owner_counter = itertools.count(max_owner + 1)

        pet_ids = [int(k.split("-")[1]) for k in self._pets.keys() if k.startswith("PET-")]
        max_pet = max(pet_ids, default=0)
        self._pet_counter = itertools.count(max_pet + 1)

        apt_ids = [int(k.split("-")[1]) for k in self._appointments.keys() if k.startswith("APT-")]
        max_apt = max(apt_ids, default=0)
        self._apt_counter = itertools.count(max_apt + 1)

    def generate_owner_id(self):
        return f"OWN-{next(self._owner_counter):04d}"

    def generate_pet_id(self):
        return f"PET-{next(self._pet_counter):04d}"

    def generate_appointment_id(self):
        return f"APT-{next(self._apt_counter):04d}"

    def register_owner(self, name, contact):
        clean_name = str(name).strip()
        clean_contact = str(contact).strip()

        if not clean_name or not clean_contact:
            raise ValueError("Owner Name and Contact Number cannot be empty.")

        owner_id = self.generate_owner_id()
        self._owners[owner_id] = {
            "owner_id": owner_id,
            "name": clean_name,
            "contact": clean_contact
        }
        self._save_to_disk()
        return owner_id

    def get_owners(self):
        return self._owners

    def add_pet(self, pet):
        clean_owner_id = str(pet.owner_id).strip()
        if clean_owner_id not in self._owners:
            raise KeyError(f"Cannot add pet: Owner ID '{clean_owner_id}' does not exist.")
        self._pets[pet.pet_id] = pet
        self._save_to_disk()

    def get_pets(self):
        return self._pets

    def schedule_appointment(self, pet_name):
        clean_pet_name = str(pet_name).strip()
        if not clean_pet_name:
            raise ValueError("Pet Name cannot be empty.")

        apt_id = self.generate_appointment_id()
        self._appointments[apt_id] = {
            "appointment_id": apt_id,
            "pet_name": clean_pet_name,
            "status": "Scheduled"
        }
        self._save_to_disk()
        return apt_id

    def update_appointment_status(self, appointment_id, status):
        clean_apt_id = str(appointment_id).strip()
        valid_statuses = {"Scheduled", "Completed", "Cancelled"}
        formatted_status = str(status).strip().capitalize()

        if formatted_status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Allowed values: {', '.join(sorted(valid_statuses))}")

        if clean_apt_id in self._appointments:
            self._appointments[clean_apt_id]["status"] = formatted_status
            self._save_to_disk()
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
        if os.path.exists(self._storage_file):
            os.remove(self._storage_file)