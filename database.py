import threading

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
        self._pets = []
        self._appointments = {}

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
        if owner_id in self._owners:
            raise ValueError(f"Owner ID '{owner_id}' already exists.")
        self._owners[owner_id] = {
            "name": name.strip(),
            "contact": contact.strip()
        }

    def get_owners(self):
        return self._owners

    def add_pet(self, pet):
        if pet.owner_id not in self._owners:
            raise KeyError(f"Cannot add pet: Owner ID '{pet.owner_id}' does not exist.")
        self._pets.append(pet)

    def get_pets(self):
        return self._pets

    def schedule_appointment(self, appointment_id, pet_name):
        if appointment_id in self._appointments:
            raise ValueError(f"Appointment ID '{appointment_id}' already exists.")
        self._appointments[appointment_id] = {
            "pet_name": pet_name.strip(),
            "status": "Scheduled"
        }

    def update_appointment_status(self, appointment_id, status):
        valid_statuses = {"Scheduled", "Completed", "Cancelled"}
        formatted_status = status.strip().capitalize()
        if formatted_status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Choose from {valid_statuses}")
        if appointment_id in self._appointments:
            self._appointments[appointment_id]["status"] = formatted_status
            return True
        return False

    def cancel_appointment(self, appointment_id):
        return self.update_appointment_status(appointment_id, "Cancelled")

    def get_appointments(self):
        return self._appointments