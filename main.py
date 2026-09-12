import sys
import unittest
from database import ClinicDatabase
from pet_factory import PetFactory
import test_clinic


def safe_input(prompt):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Returning to the menu.")
        return ""


def read_menu_choice(prompt):
    while True:
        value = safe_input(prompt).strip().lower()
        if value == "":
            print("No option selected. Press a valid key and then Enter.")
            return ""
        return value


def read_required_input(prompt, field_name):
    while True:
        value = safe_input(prompt).strip()
        if value != "":
            return value
        print(f"{field_name} cannot be empty. Please press a valid value and then Enter.")


def run_tests():
    print("\n" + "=" * 40)
    print("Running Automated Unit Tests")
    print("=" * 40)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_clinic)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def main():
    db = ClinicDatabase.get_instance()

    while True:
        print("\n=== Veterinary Clinic Management System ===")
        print("a. Pet Owner Management")
        print("b. Pet Management (Factory implementation)")
        print("c. Appointment Management")
        print("d. Run Unit Tests")
        print("e. Exit")

        choice = read_menu_choice("\nEnter your choice: ")
        if choice == "":
            continue

        if choice == "a":
            print("\nPet Owner Management")
            print("a. Register Owner")
            print("b. View Owners")
            sub = read_menu_choice("Select option: ")
            if sub == "":
                continue

            if sub == "a":
                name = read_required_input("Enter Owner Name: ", "Owner Name")
                contact = read_required_input("Enter Contact Number: ", "Contact Number")
                try:
                    generated_id = db.register_owner(name, contact)
                    print(f"Owner '{name}' registered successfully with Auto-Generated ID: {generated_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif sub == "b":
                owners = db.get_owners()
                print("\nRegistered Owners:")
                if not owners:
                    print("  No registered owners found.")
                else:
                    for owner_id, info in owners.items():
                        print(f"  Owner ID: {owner_id} | Name: {info['name']} | Contact: {info['contact']}")

        elif choice == "b":
            print("\nPet Management")
            print("a. Add Pet Record")
            print("b. View Pets")
            sub = read_menu_choice("Select option: ")
            if sub == "":
                continue

            if sub == "a":
                ptype = read_required_input("Enter pet type (Dog, Cat, Bird, Rabbit): ", "Pet type")
                pname = read_required_input("Enter pet name: ", "Pet name")
                oid = read_required_input("Enter Owner ID: ", "Owner ID")
                try:
                    pet_id = db.generate_pet_id()
                    pet_obj = PetFactory.create_pet(pet_id, ptype, pname, oid)
                    db.add_pet(pet_obj)
                    print(f"Successfully created and associated {pet_obj.pet_type} '{pet_obj.name}' (ID: {pet_obj.pet_id}) with Owner {oid}!")
                except (ValueError, KeyError) as e:
                    print(f"Error: {e}")
            elif sub == "b":
                pets = db.get_pets()
                print("\nRegistered Pets:")
                if not pets:
                    print("  No registered pets found.")
                else:
                    for pet_id, pet in pets.items():
                        print(f"  Pet ID: {pet.pet_id} | Type: {pet.pet_type} | Name: {pet.name} | Owner ID: {pet.owner_id} | Sound: {pet.speak()}")

        elif choice == "c":
            print("\nAppointment Management")
            print("a. Schedule Appointment")
            print("b. View Appointments")
            print("c. Update/Cancel Appointment")
            sub = read_menu_choice("Select option: ")
            if sub == "":
                continue

            if sub == "a":
                pet_name = read_required_input("Enter Pet Name: ", "Pet Name")
                try:
                    apt_id = db.schedule_appointment(pet_name)
                    print(f"Appointment scheduled successfully with Auto-Generated ID: {apt_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif sub == "b":
                appointments = db.get_appointments()
                print("\nScheduled Appointments:")
                if not appointments:
                    print("  No scheduled appointments found.")
                else:
                    for apt_id, info in appointments.items():
                        print(f"  Appointment ID: {apt_id} | Pet Name: {info['pet_name']} | Status: {info['status']}")
            elif sub == "c":
                apt_id = read_required_input("Enter Appointment ID to update: ", "Appointment ID")
                status = read_required_input("Enter status (Scheduled, Completed, Cancelled): ", "Status")
                try:
                    if db.update_appointment_status(apt_id, status):
                        print(f"Appointment {apt_id} status updated to {status.capitalize()}.")
                    else:
                        print("Appointment ID not found.")
                except ValueError as e:
                    print(f"Error: {e}")

        elif choice == "d":
            run_tests()

        elif choice == "e":
            print("\nExiting application...")
            sys.exit(0)

        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()