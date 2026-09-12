<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:38BDF8,100:6366F1&height=200&section=header&text=Paws%20%26%20Care%20Veterinary%20Clinic&fontSize=38&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Appointment%20Management%20System&descAlignY=55&descAlign=50" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1000&color=6366F1&center=true&vCenter=true&width=700&lines=Singleton+%2B+Factory+Design+Patterns;Thread-Safe+In-Memory+Repository;Polymorphic+Pet+Creation+%F0%9F%90%B6%F0%9F%90%B1%F0%9F%90%A6%F0%9F%90%B0;22%2B+Automated+Unit+Tests+with+unittest" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Design Pattern](https://img.shields.io/badge/Pattern-Singleton-6366F1?style=for-the-badge)
![Design Pattern](https://img.shields.io/badge/Pattern-Factory-38BDF8?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-unittest-22C55E?style=for-the-badge&logo=pytest&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</div>

---

## 📖 Table of Contents

- [Academic Information](#-academic-information)
- [Project Overview](#-project-overview)
- [Architecture at a Glance](#-architecture-at-a-glance)
- [Booking Flow (Sequence Diagram)](#-booking-flow-sequence-diagram)
- [Project Structure](#-project-structure)
- [Task Distribution](#-task-distribution)
- [Setup and Installation](#-setup-and-installation)
- [Usage](#-usage)
- [Running Unit Tests](#-running-unit-tests-directly)

---

## 🎓 Academic Information

<table>
<tr><td><b>Course</b></td><td>CPE106L-4 Software Design Laboratory</td></tr>
<tr><td><b>Laboratory Exercise</b></td><td>Laboratory Report 4 — Design Patterns and Unit Testing</td></tr>
<tr><td><b>Program</b></td><td>BS Computer Engineering</td></tr>
<tr><td><b>Institution</b></td><td>Mapúa University</td></tr>
<tr><td><b>Collaborators</b></td><td>Edmarc Justin C. Oabel · Jabez Molar </td></tr>
</table>

---

## 🐾 Project Overview

Paws and Care Veterinary Clinic requires an automated appointment management system to reduce scheduling conflicts and streamline pet record tracking.

This project demonstrates two core design patterns and automated verification:

| Concept | Description |
|---|---|
| 🔒 **Singleton Pattern** | Manages a single, centralized in-memory clinic repository (`ClinicDatabase`) with thread-safe double-checked locking and auto-increment identifier counters. |
| 🏭 **Factory Pattern** | Provides an extensible interface (`PetFactory`) to instantiate polymorphic pet objects (`Dog`, `Cat`, `Bird`, `Rabbit`) without exposing concrete instantiation logic. |
| ✅ **Automated Unit Testing** | Complete test coverage via Python's built-in `unittest` framework validating singleton integrity, record registration, scheduling workflows, and status transitions. |
| 💾 **Persistence** | Auto-saves records to a local `clinic_data.json` storage file to maintain state between application restarts. |

---

## 🏗 Architecture at a Glance

```mermaid
classDiagram
    class ClinicDatabase {
        -_instance: ClinicDatabase$
        -_lock: Lock$
        -owners: dict
        -pets: dict
        -appointments: dict
        +__new__() ClinicDatabase
        +add_owner(name, contact) dict
        +add_pet(record) dict
        +add_appointment(pet_id, owner_id, reason, schedule) dict
        +update_appointment_status(id, status) bool
        +save_to_disk()
        +_load_from_disk()
    }

    class Pet {
        <<abstract>>
        +name: str
        +breed: str
        +age: int
        +owner_id: str
        +checkup_notes()* str
        +to_record() dict
    }

    class Dog { +checkup_notes() str }
    class Cat { +checkup_notes() str }
    class Bird { +checkup_notes() str }
    class Rabbit { +checkup_notes() str }

    class PetFactory {
        -_registry: dict$
        +create_pet(species, name, breed, age, owner_id)$ Pet
        +supported_species()$ list
        +register_species(key, cls)$
    }

    Pet <|-- Dog
    Pet <|-- Cat
    Pet <|-- Bird
    Pet <|-- Rabbit
    PetFactory ..> Pet : creates
    ClinicDatabase o-- Pet : stores as record
```

---

## 🔁 Booking Flow (Sequence Diagram)

```mermaid
sequenceDiagram
    actor User
    participant CLI as main.py (CLI)
    participant Factory as PetFactory
    participant DB as ClinicDatabase (Singleton)
    participant Disk as clinic_data.json

    User->>CLI: Select "b. Pet Management"
    CLI->>Factory: create_pet(species, name, breed, age, owner_id)
    Factory-->>CLI: Pet instance (Dog/Cat/Bird/Rabbit)
    CLI->>DB: add_pet(pet.to_record())
    DB->>DB: generate PET-XXXX id
    DB->>Disk: save_to_disk()
    DB-->>CLI: pet record

    User->>CLI: Select "c. Appointment Management"
    CLI->>DB: add_appointment(pet_id, owner_id, reason, schedule)
    DB->>DB: generate APT-XXXX id (status=Scheduled)
    DB->>Disk: save_to_disk()
    DB-->>CLI: appointment record
    CLI-->>User: Confirmation message
```

---

## 📂 Project Structure

```text
cpe106l-lab4-vet-clinic/
│
├── database.py       # Thread-safe Singleton database with ID generation & JSON persistence
├── pet_factory.py    # Pet abstraction and Factory pattern implementations
├── test_clinic.py    # Automated unit test suite (unittest)
├── main.py           # Command-Line Interface (CLI) navigation and test runner
└── README.md         # Project documentation
```

---

## 👥 Task Distribution

| Team Member | Role | Responsibilities |
| --- | --- | --- |
| **Edmarc Justin C. Oabel** | Person A (Core Architecture & Models) | Designed and implemented `database.py` (Singleton pattern, synchronized sequence counters, and JSON file persistence) and `pet_factory.py` (abstract Pet base class and PetFactory). |
| **Jabez Molar** | Person B (CLI & Automated Testing) | Implemented `main.py` (interactive CLI workflow and input handling) and `test_clinic.py` (test suite covering database assertions, factory instantiation, and appointment flows). |

---

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.9 or newer installed on your machine.
- Git installed and configured.
- Visual Studio Code (or any preferred code editor).

### Clone the Repository

```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/cpe106l-lab4-vet-clinic.git
cd cpe106l-lab4-vet-clinic
```

---

## 🚀 Usage

### Run the Application

To launch the interactive CLI:

```bash
python main.py
```

### CLI Menu Options

<details open>
<summary><b>a. Pet Owner Management</b></summary>
<br/>
Register a pet owner (auto-generates <code>OWN-XXXX</code>) and view existing owners.
</details>

<details open>
<summary><b>b. Pet Management (Factory implementation)</b></summary>
<br/>
Create and associate a pet record using <code>PetFactory</code> (auto-generates <code>PET-XXXX</code>).
</details>

<details open>
<summary><b>c. Appointment Management</b></summary>
<br/>
Book a visit (auto-generates <code>APT-XXXX</code>), view schedules, and update status (<code>Scheduled</code>, <code>Completed</code>, <code>Cancelled</code>).
</details>

<details open>
<summary><b>d. Run Unit Tests</b></summary>
<br/>
Execute the automated test suite directly from the CLI.
</details>

<details open>
<summary><b>e. Exit</b></summary>
<br/>
Close the application session.
</details>

---

## 🧪 Running Unit Tests Directly

Run the unit test runner in verbose mode:

```bash
python -m unittest -v test_clinic
```

<div align="center">

![Tests Passing](https://img.shields.io/badge/22%20tests-passing-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6366F1,100:38BDF8&height=100&section=footer" width="100%"/>

</div>
