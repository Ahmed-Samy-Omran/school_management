from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "School Student"
    _order = "admission_number, id"  # that for ordering the records by admission number and then by id

    # constarints
  # Odoo 19 Database Constraint
    _admission_number_unique = models.Constraint(
        "unique(admission_number)",
        "The admission number must be unique!",
    )

    # fields
    name = fields.Char(required=True, string="Student Name", index=True)
    admission_number = fields.Char(
        string="Admission Number", required=True, copy=False, index=True
    )  # delete teh default value because it will make error incase i save the record and the default value is already exist in the database
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
    )
    date_of_birth = fields.Date(string="Date of Birth")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    active = fields.Boolean(
        string="Active", default=True
    )  # here we dont put required because it will be defaulted to true or false
    age = fields.Integer(
        string="Age", compute="_compute_age"
    )  # i delete store=True because it will store the value in the database and we want it to be computed every time we call it it will change after a year beacuse it depnd on the date of birth


    # compute method for age
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for student in self:
            if student.date_of_birth:
                student.age=relativedelta(  #realtivedelta : 
                    today,
                    student.date_of_birth
                ).years
            else:
                student.age=0


    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        today=fields.Date.today()
        for student in self:
            if student.date_of_birth and student.date_of_birth>today:   
                raise ValidationError("The date of birth cannot be in the future.")



