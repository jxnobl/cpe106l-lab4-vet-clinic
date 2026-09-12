import sys
import unittest
from database import ClinicDatabase
from pet_factory import PetFactory
import test_clinic

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

        choice = input("\nEnter your choice: ").strip()

        if choice == "a":
            print("\nPet Owner Management")
            print("a. Register Owner")
            print("b. View Owners")
            sub = input("Select option: ").strip().lower()

            if sub == "a":
                oid = input("Enter Owner ID: ").strip()
                name = input("Enter Owner Name: ").strip()
                contact = input("Enter Contact Number: ").strip()
                try:
                    db.register_owner(oid, name, contact)
                    print(f"Owner '{name}' registered successfully!")
                except ValueError as e:
                    print(f"Error: {e}")
            elif sub == "b":
                print("Registered Owners:", db.get_owners())

        elif choice == "b":
            print("\nPet Management")
            print("a. Add Pet Record")
            print("b. View Pets")
            sub = input("Select option: ").strip().lower()

            if sub == "a":
                ptype = input("Enter pet type (Dog, Cat, Bird, Rabbit): ").strip()
                pname = input("Enter pet name: ").strip()
                oid = input("Enter owner ID: ").strip()
                try:
                    pet_obj = PetFactory.create_pet(ptype, pname, oid)
                    db.add_pet(pet_obj)
                    print(f"Successfully created and associated a {pet_obj.pet_type} named '{pet_obj.name}'!")
                except (ValueError, KeyError) as e:
                    print(f"Error: {e}")
            elif sub == "b":
                print("Registered Pets:", db.get_pets())

        elif choice == "c":
            print("\nAppointment Management")
            print("a. Schedule Appointment")
            print("b. View Appointments")
            print("c. Update/Cancel Appointment")
            sub = input("Select option: ").strip().lower()

            if sub == "a":
                apt_id = input("Enter Appointment ID: ").strip()
                pet_name = input("Enter Pet Name: ").strip()
                try:
                    db.schedule_appointment(apt_id, pet_name)
                    print("Appointment scheduled successfully!")
                except ValueError as e:
                    print(f"Error: {e}")
            elif sub == "b":
                print("Appointments:", db.get_appointments())
            elif sub == "c":
                apt_id = input("Enter Appointment ID: ").strip()
                status = input("Enter status (Scheduled, Completed, Cancelled): ").strip()
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