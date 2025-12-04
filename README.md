![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![OOP](https://img.shields.io/badge/Architecture-OOP-green)
![CRUD](https://img.shields.io/badge/Features-CRUD-orange)
![Testing](https://img.shields.io/badge/Testing-pytest-blue?logo=pytest)
![CLI](https://img.shields.io/badge/Interface-Console-lightgrey)

#  **Client Information Management System (Python + SQLite)**

## 📌 Overview

This project is a **console-based Client Information Management System** developed as part of my *Software Engineering Fundamentals* module.
It demonstrates key software engineering practices, including:

* Object-oriented design
* Relational database modelling
* CRUD operations
* Data validation and error handling
* Use of UML diagrams
* Automated unit testing using `pytest`
* Agile-influenced development workflow
* Source control (Bitbucket + Git)

The system allows Mediaworks employees to **log in**, view, search, update, add and delete client data stored in a local SQLite database.
Access is permission-based, ensuring only authorised users can perform admin functionality.

Full project documentation is included in the repository:
📄 *“Final Assessment Write Up”* 

---

## 🚀 Features

### 👤 **User Login & Role Permissions**

* Username-based authentication
* Two roles:

  * **Employee** – read-only access
  * **Admin** – full CRUD access
* User permissions stored in `users` table
* Hard-coded starter records auto-added if database is empty

---

### 🗂 **Client Record Management (CRUD)**

Each client has:

* Client ID (primary key)
* Client name
* Contract status
* Contract start & end dates
* Whether project-based work is included
* HQ longitude & latitude
* Estimated total revenue

Admins can:

* **Add** new client records
* **Amend** existing fields (datatype-validated)
* **Delete** client records (with confirmation)
* **Search** by any column

Employees can:

* **Search** only

All input is validated for datatype, length, and schema consistency.

---

### 🔎 **Search System**

* Search by any attribute
* Returns zero, one, or many matching records
* Results displayed using `pandas` for improved readability

---

### 🧪 **Testing**

Includes a full test suite using **pytest**, covering:

* Datatype comparison
* Input conversion
* Column validation
* Database queries
* User and Client class behaviour
* Table lookups and permission logic

Testing uses **in-memory SQLite databases** for speed and isolation.

See *Appendix 1 – Test Scripts* in the write-up.


---

### 🧱 **Architecture**

#### Object-Oriented Design

Two primary classes:

* `User` – stores username, permission level, login status
* `Client` – stores all client attributes with setter/getter methods

#### Database

SQLite database containing:

* `users`
* `clients`

Designed for simplicity, portability, and zero-configuration deployment.

#### UML diagrams (in write-up):

* Use Case
* Activity diagram
* Class diagram
* Program structure chart

These ensured requirements clarity and prevented scope creep.


---

## 📦 Installation & Setup

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/IsaacPatrickson/client-information-management-system.git
cd <repo-name>
```

### 2️⃣ **Install Dependencies**

```bash
pip install pandas pytest
```

SQLite is included by default with Python.

---

## ▶️ Running the Application

Run the main program:

```bash
python main.py
```

On first launch, the system will automatically:

* Create the SQLite database
* Create the `users` and `clients` tables
* Insert default seed data if empty

---

## 🎮 How to Use

### 🔐 Login Menu

```
1. Login
0. Quit
```

After entering a valid username stored in the database:

### 👨‍💼 Admin Menu (permission ≥5)

```
1. Amend client information
2. Add a client
3. Delete a client
4. Search for clients
0. Log out
```

### 👨‍💻 Employee Menu (permission <5)

```
1. Search for clients
0. Log out
```

All operations give clear feedback and validation prompts.

---

## 🔮 Future Improvements

If developed further, the application could include:

* Password-based login with secure hashing
* GUI interface (Tkinter or PyQt)
* Migrating to a web app (Flask or Django)
* Role/permission management UI
* Audit logs
* Input sanitisation and stricter validation
* Database upgrades to MySQL or PostgreSQL

---

## 🧠 Lessons Learned

Key insights from development:

* UML diagrams helped avoid scope creep
* Automated tests are far more efficient than manual testing
* SQLite is ideal for small systems with zero configuration
* Following Agile fully requires better task breakdown
* TDD would have caught issues earlier

Detailed reflection in *Task 4 – Review and Reflection*.


---

## 👤 Author

**Isaac Patrickson**
University of Roehampton – DTS Degree Apprentice
Software Engineering Fundamentals Project

GitHub: *github.com/IsaacPatrickson*
Email: *[isaacspatrickson@gmail.com](mailto:isaacspatrickson@gmail.com)*
