from abc import ABC, abstractmethod

class Pet(ABC):
    def __init__(self, pet_type, name, owner_id):
        self.pet_type = pet_type
        self.name = name.strip()
        self.owner_id = str(owner_id).strip()

    @abstractmethod
    def speak(self):
        pass

    def __repr__(self):
        return f"{self.pet_type}(Name='{self.name}', OwnerID='{self.owner_id}', Sound='{self.speak()}')"

class Dog(Pet):
    def __init__(self, name, owner_id):
        super().__init__("Dog", name, owner_id)

    def speak(self):
        return "Woof!"

class Cat(Pet):
    def __init__(self, name, owner_id):
        super().__init__("Cat", name, owner_id)

    def speak(self):
        return "Meow!"

class Bird(Pet):
    def __init__(self, name, owner_id):
        super().__init__("Bird", name, owner_id)

    def speak(self):
        return "Chirp!"

class Rabbit(Pet):
    def __init__(self, name, owner_id):
        super().__init__("Rabbit", name, owner_id)

    def speak(self):
        return "Squeak!"

class PetFactory:
    _pet_registry = {
        "dog": Dog,
        "cat": Cat,
        "bird": Bird,
        "rabbit": Rabbit
    }

    @classmethod
    def create_pet(cls, pet_type, name, owner_id):
        normalized = pet_type.strip().lower()
        if normalized not in cls._pet_registry:
            raise ValueError(f"Pet type '{pet_type}' is not supported.")
        return cls._pet_registry[normalized](name, owner_id)