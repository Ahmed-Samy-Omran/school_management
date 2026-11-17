# 🎓 School Management — Odoo 19

![Odoo](https://img.shields.io/badge/Odoo-19.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)

A standalone **Odoo 19** module to manage students and basic school operations.
This repository contains **only** the `school_management` module.

---

## 📌 Overview

The module adds a **School Management** application to Odoo with a complete
student registry: registration, personal information, contact details, age
computation, archiving, searching and filtering.

| Feature | Description |
| --- | --- |
| Student registration | Create, edit and archive student records |
| Unique admission number | Database-level `unique` constraint per student |
| Auto-computed age | Derived from date of birth, always up to date |
| Date validation | Future dates of birth are rejected |
| Search & filters | Search by name / admission no. / email, filter active & archived, group by gender |
| Multi-user access | Access rights defined for internal users |

---

## 🧩 Module Architecture

```mermaid
flowchart TD
    A["School Management<br/>(Odoo 19 addon)"] --> B["Models"]
    A --> C["Views"]
    A --> D["Security"]
    A --> E["Menus"]

    B --> B1["school.student"]
    B1 --> B1a["Fields<br/>name, admission_number, gender,<br/>date_of_birth, email, phone, active"]
    B1 --> B1b["Computed<br/>age (_compute_age)"]
    B1 --> B1c["Constraints<br/>unique(admission_number)<br/>date_of_birth not in future"]

    C --> C1["List View"]
    C --> C2["Form View"]
    C --> C3["Search View<br/>filters + group by"]
    C --> C4["Window Action<br/>action_school_student"]

    D --> D1["ir.model.access.csv<br/>base.group_user: R/W/C/D"]

    E --> E1["School Management"]
    E1 --> E2["Students"]

    C4 --> E2
```

---

## 🗃️ Data Model

```mermaid
classDiagram
    class school_student {
        +Char name
        +Char admission_number  «unique»
        +Selection gender
        +Date date_of_birth
        +Char email
        +Char phone
        +Boolean active
        +Integer age  «computed»
        +_compute_age()
        +_check_date_of_birth()
    }
```

**Constraints**

- `admission_number` must be unique across all students (DB constraint).
- `date_of_birth` cannot be a future date (`ValidationError`).
- `age` is computed on the fly from `date_of_birth` (not stored), so it always
  reflects the student's current age.

---

## 📂 Project Structure

```text
school_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── student.py
├── security/
│   └── ir.model.access.csv
├── views/
│   └── student_views.xml
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

1. Copy the `school_management` folder into your Odoo **addons** path, e.g.:

   ```bash
   git clone https://github.com/Ahmed-Samy-Omran/school_management.git
   ```

2. Restart the Odoo server.
3. In Odoo: **Apps → Update Apps List**.
4. Search for **School Management System** and click **Install**.

> Requires Odoo **19.0** and Python **3.10+**.

---

## 🚀 Usage

1. Open the **School Management** app from the main menu.
2. Go to **Students → New**.
3. Fill in the student name and admission number (required).
4. Add date of birth — the **age** field is calculated automatically.
5. Use the search bar to find students, filter **Active / Archived**, or
   **group by gender**.

---

## 🗺️ Roadmap

```mermaid
graph LR
    A["✅ Module skeleton"] --> B["✅ Student model"]
    B --> C["✅ Views & menus"]
    C --> D["✅ Access rights"]
    D --> E["✅ Search & filters"]
    E --> F["⬜ Teachers & classes"]
    F --> G["⬜ Enrollment & attendance"]
    G --> H["⬜ Grades & reports"]
```

- [x] Module skeleton & manifest
- [x] Student model with computed age and constraints
- [x] List / form / search views and menus
- [x] Security access rights
- [x] Search filters and grouping
- [ ] Teachers & classes
- [ ] Enrollment & attendance
- [ ] Grades & reports

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

```bash
git checkout -b feature/my-feature
git commit -m "Add my feature"
git push origin feature/my-feature
```

---

## 📄 License

This project is licensed under **LGPL-3**.

## 👤 Author

**Ahmed Omran** — [@Ahmed-Samy-Omran](https://github.com/Ahmed-Samy-Omran)
