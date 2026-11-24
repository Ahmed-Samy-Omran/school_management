from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Teacher"
    _order = "employee_number, id"

    # constraints
    _employee_number_unique = models.Constraint(
        "unique(employee_number)",
        "The employee number must be unique!",
    )

    # fields
    name = fields.Char(required=True, string="Teacher Name", index=True)
    employee_number = fields.Char(
        required=True, string="Employee Number", copy=False, index=True
    )
    contact_summary = fields.Char(
        string="Contact Summary", compute="_compute_contact_summary", store=True
    )
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    hire_date = fields.Date(
        string="Hire Date",
        required=True,
        default=fields.Date.context_today,
    )
    specialization = fields.Selection(
        [
            ("mathematics", "Mathematics"),
            ("science", "Science"),
            ("english", "English"),
            ("arabic", "Arabic"),
            ("history", "History"),
            ("geography", "Geography"),
            ("computer_science", "Computer Science"),
            ("other", "Other"),
        ],
        string="Specialization",
        required=True,
        default="other",
    )

    employment_type = fields.Selection(
        [
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("contract", "Contract"),
        ],
        string="Employment Type",
        required=True,
        default="full_time",
    )

    years_of_service = fields.Integer(
        string="Years of Service", compute="_compute_years_of_service"
    )
    active = fields.Boolean(string="Active", default=True)

    @api.constrains("hire_date")
    def _check_hire_date(self):
        today = fields.Date.today()
        for teacher in self:
            if teacher.hire_date and teacher.hire_date > today:
                raise ValidationError("The hire date cannot be in the future.")

    @api.depends("hire_date")
    def _compute_years_of_service(self):
        today = fields.Date.today()
        for teacher in self:
            if teacher.hire_date and teacher.hire_date <= today:
                teacher.years_of_service = relativedelta(today, teacher.hire_date).years
            else:
                teacher.years_of_service = 0

    @api.depends("email", "phone")
    def _compute_contact_summary(self):
        for teacher in self:
            contact_info = []
            if teacher.email:
                contact_info.append(f"Email: {teacher.email}")
            if teacher.phone:
                contact_info.append(f"Phone: {teacher.phone}")
            teacher.contact_summary = (
                " | ".join(contact_info)
                if contact_info
                else "No contact information available."
            )

    @api.constrains("email")
    def _check_email(self):
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        for record in self:
            if record.email and not re.fullmatch(email_pattern, record.email):
                raise ValidationError("Please enter a valid email address.")
