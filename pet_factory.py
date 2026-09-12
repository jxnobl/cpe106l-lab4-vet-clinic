from abc import ABC, abstractmethod


class Pet(ABC):
    def __init__(self, pet_id, pet_type, name, owner_id):
        self.pet_id = str(pet_id).strip() if pet_id is not None else ""
        self.pet_type = pet_type
        self.name = name.strip()
        self.owner_id = str(owner_id).strip()

    @abstractmethod
    def speak(self):
        pass

    def __repr__(self):
        return f"{self.pet_type}(Name='{self.name}', OwnerID='{self.owner_id}', Sound='{self.speak()}')"


class Dog(Pet):
    def __init__(self, name, owner_id, pet_id=None):
        super().__init__(pet_id, "Dog", name, owner_id)

    def speak(self):
        return "Woof!"


class Cat(Pet):
    def __init__(self, name, owner_id, pet_id=None):
        super().__init__(pet_id, "Cat", name, owner_id)

    def speak(self):
        return "Meow!"


class Bird(Pet):
    def __init__(self, name, owner_id, pet_id=None):
        super().__init__(pet_id, "Bird", name, owner_id)

    def speak(self):
        return "Chirp!"


class Rabbit(Pet):
    def __init__(self, name, owner_id, pet_id=None):
        super().__init__(pet_id, "Rabbit", name, owner_id)

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
    def create_pet(cls, *args):
        if len(args) == 3:
            pet_type, name, owner_id = args
            pet_id = None
        elif len(args) == 4:
            pet_id, pet_type, name, owner_id = args
        else:
            raise TypeError("create_pet expects either (pet_type, name, owner_id) or (pet_id, pet_type, name, owner_id)")

        normalized = str(pet_type).strip().lower()
        if normalized not in cls._pet_registry:
            raise ValueError(f"Pet type '{pet_type}' is not supported.")

        pet_class = cls._pet_registry[normalized]
        return pet_class(name, owner_id, pet_id=pet_id)