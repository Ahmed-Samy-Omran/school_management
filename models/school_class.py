from odoo import models, fields, api

class SchoolClass(models.Model):
    _name = "school.class"
    _description = "School Class"
    _order = "code desc, name"

    _code_unique=models.Constraint(
        "unique(code)",
        "The code must be unique!"
    )

    name=fields.Char(string="Class Name", required=True, index=True)
    code=fields.Char(required=True, index=True,copy=False,string="Class Code")
    description=fields.Text(string="Description")
    sequence=fields.Integer(string="Sequence", default=10)
    active=fields.Boolean(string="Active", default=True)
    section_ids=fields.One2many(
        "school.section",
        "class_id",
        string="Sections"
    )
    section_count=fields.Integer(string="Section Count", compute="_compute_section_count")
    @api.depends('section_ids')
    def _compute_section_count(self):
        for school_class in self:
            school_class.section_count=len(school_class.section_ids) #it get the sections related to the class and count them and assign the value to section_count field