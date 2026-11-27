from attrs import field

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolSection(models.Model):
    _name = "school.section"
    _description = "School Section"
    _order = "code desc, name"

    _code_unique = models.Constraint("unique(code)", "The code must be unique!")

    name = fields.Char(string="Section Name", required=True, index=True)
    code = fields.Char(required=True, index=True, copy=False, string="Section Code")
    capacity = fields.Integer(
        string="Capacity", required=True, default=30
    )  # Maximum number of students
    student_count = fields.Integer(
        string="Student Count", compute="_compute_student_count"
    )
    available_seats = fields.Integer(
        string="Available Seats", compute="_compute_available_seats"
    )
    # Stored so search filters can use it in domains (computed fields need store=True).
    is_full = fields.Boolean(string="Is Full", compute="_compute_is_full", store=True)
    active = fields.Boolean(string="Active", default=True)

    class_id = fields.Many2one(
        "school.class", string="Class", required=True, ondelete="restrict", index=True
    )

    academic_year_id = fields.Many2one(
        "school.academic_year",
        string="Academic Year",
        required=True,
        ondelete="restrict",
        index=True,
    )
    #many section to one teacher
    class_teacher_id = fields.Many2one(  
        "school.teacher",
        string="Class Teacher",
        ondelete="restrict",
        index=True,
    )

    student_ids = fields.One2many("school.student", "section_id", string="Students")

    @api.constrains("capacity","student_ids")
    def _check_capacity(self):
        for section in self:
            if section.capacity <= 0:
                raise ValidationError("Capacity must be greater than zero.")
            if len(section.student_ids) > section.capacity:
                raise ValidationError(
                    "The section cannot contain more students than its capacity."
                )




    @api.depends("capacity", "student_ids")
    def _compute_available_seats(self):
        for section in self:
            section.available_seats = max(section.capacity - len(section.student_ids), 0)

    @api.depends("capacity", "student_ids")
    def _compute_is_full(self):
        for section in self:
            section.is_full = len(section.student_ids) >= section.capacity


    @api.depends("student_ids")
    def _compute_student_count(self):
        for section in self:
            section.student_count = len(section.student_ids)



    
