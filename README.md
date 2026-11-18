# 🎓 School Management — Odoo 19

![Odoo](https://img.shields.io/badge/Odoo-19.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)

A standalone **Odoo 19** module to manage students, teachers and basic school
operations. This repository contains **only** the `school_management` module.

---

## 📌 Overview

The module adds a **School Management** application to Odoo with two registries:

- **Students** — registration, personal data, computed age and archiving.
- **Teachers** — employment data, specialization, computed years of service,
  contact summary and email validation.

| Feature | Description |
| --- | --- |
| Student registration | Create, edit and archive student records |
| Teacher registration | Create, edit and archive teacher records |
| Unique identifiers | `unique(admission_number)` and `unique(employee_number)` at DB level |
| Auto-computed age | Derived from the student's date of birth, always up to date |
| Auto-computed years of service | Derived from the teacher's hire date |
| Contact summary | Teacher email/phone summarized in one stored field |
| Validations | Future dates and invalid emails are rejected |
| Search & filters | Name / number / email search, active-archived filters, grouping |
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

    B --> B2["school.teacher"]
    B2 --> B2a["Fields<br/>name, employee_number, email, phone,<br/>hire_date, specialization, employment_type"]
    B2 --> B2b["Computed<br/>years_of_service, contact_summary"]
    B2 --> B2c["Constraints<br/>unique(employee_number)<br/>hire_date not in future<br/>valid email format"]

    C --> C1["Student Views<br/>list · form · search"]
    C --> C2["Teacher Views<br/>list · form · search"]
    C --> C3["Window Actions<br/>action_school_student<br/>action_school_teacher"]

    D --> D1["ir.model.access.csv<br/>base.group_user: R/W/C/D"]

    E --> E1["School Management"]
    E1 --> E2["Students"]
    E1 --> E3["Teachers"]

    C1 --> E2
    C2 --> E3
```

---

## 🗃️ Data Model

```mermaid
classDiagram
    class school_student {
        +Char name
        +Char admission_number «unique»
        +Selection gender
        +Date date_of_birth
        +Char email
        +Char phone
        +Boolean active
        +Integer age «computed»
        +_compute_age()
        +_check_date_of_birth()
    }

    class school_teacher {
        +Char name
        +Char employee_number «unique»
        +Char email
        +Char phone
        +Date hire_date
        +Selection specialization
        +Selection employment_type
        +Boolean active
        +Integer years_of_service «computed»
        +Char contact_summary «computed, stored»
        +_check_hire_date()
        +_compute_years_of_service()
        +_compute_contact_summary()
        +_check_email()
    }
```

### `school.teacher` fields

| Field | Type | Notes |
| --- | --- | --- |
| `name` | Char | Required, indexed |
| `employee_number` | Char | Required, unique, not copied |
| `email` / `phone` | Char | Optional contact data |
| `contact_summary` | Char | Computed & stored from email/phone |
| `hire_date` | Date | Required, defaults to today, cannot be in the future |
| `specialization` | Selection | Mathematics, Science, English, Arabic, History, Geography, Computer Science, Other |
| `employment_type` | Selection | Full Time, Part Time, Contract |
| `years_of_service` | Integer | Computed from `hire_date` (not stored) |
| `active` | Boolean | Enables archive/unarchive |

### Business rules

```mermaid
flowchart TD
    Save([Create / edit teacher]) --> D{Hire date<br/>in the future?}
    D -- Yes --> Err1[ValidationError]
    D -- No --> C1[Compute years_of_service<br/>relativedelta today - hire_date]
    C1 --> C2[Compute contact_summary<br/>email + phone, stored]
    C2 --> E{Email matches<br/>regex format?}
    E -- No --> Err2[ValidationError]
    E -- Yes --> OK([Record saved])
```

**Constraints**

- `school.student.admission_number` must be unique (DB constraint).
- `school.teacher.employee_number` must be unique (DB constraint).
- `date_of_birth` and `hire_date` cannot be future dates (`ValidationError`).
- Teacher `email`, when filled, must match a valid email pattern.
- `age` and `years_of_service` are computed on the fly, so they stay accurate
  over time.

---

## 📂 Project Structure

```text
school_management/
├── __init__.py
├── __manifest__.py
├── LICENSE
├── models/
│   ├── __init__.py
│   ├── student.py
│   └── teacher.py
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── student_views.xml
│   └── teacher_views.xml
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

1. Clone the module into your Odoo **addons** path:

   ```bash
   git clone https://github.com/Ahmed-Samy-Omran/school_management.git
   ```

2. Restart the Odoo server.
3. In Odoo: **Apps → Update Apps List**.
4. Search for **School Management System** and click **Install**.

> Requires Odoo **19.0**.

---

## 🚀 Usage

1. Open the **School Management** app from the main menu.
2. **Students → New**: fill the name and admission number (required), add the
   date of birth and the age is computed automatically.
3. **Teachers → New**: fill the name, employee number, hire date,
   specialization and employment type — years of service and contact summary
   are computed for you.
4. Use the search bar to filter **Active / Archived**, filter by employment
   type or specialization, and group by gender / specialization.

---

## 🗺️ Roadmap

```mermaid
graph LR
    A["✅ Module skeleton"] --> B["✅ Student model"]
    B --> C["✅ Student views & menus"]
    C --> D["✅ Access rights"]
    D --> E["✅ Search & filters"]
    E --> F["✅ Teacher model, views & rules"]
    F --> G["⬜ Classes & enrollment"]
    G --> H["⬜ Attendance"]
    H --> I["⬜ Grades & reports"]
```

- [x] Module skeleton & manifest
- [x] Student model with computed age and constraints
- [x] Student list / form / search views and menus
- [x] Security access rights
- [x] Search filters and grouping
- [x] Teacher model: unique employee number, computed service years, contact summary, email validation
- [x] Teacher list / form / search views, action and menu
- [ ] Classes & enrollment
- [ ] Attendance
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

This project is licensed under **LGPL-3** — see the [LICENSE](LICENSE) file.

## 👤 Author

**Ahmed Omran** — [@Ahmed-Samy-Omran](https://github.com/Ahmed-Samy-Omran)
