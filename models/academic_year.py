from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcademicYear(models.Model):
    _name = "school.academic_year"
    _description = "Academic Year"
    _order = "date_start desc, code"

    # Constraints
    _code_unique = models.Constraint(
        "unique(code)",
        "The code must be unique!",
    )

    # Fields
    name = fields.Char(string="Academic Year", required=True, index=True)
    code = fields.Char(string="Code", required=True, index=True, copy=False)
    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)
    is_current = fields.Boolean(string="Is Current", default=False)
    active = fields.Boolean(string="Active", default=True)
    duration_days = fields.Integer(string="Duration (Days)", compute="_compute_duration_days", store=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("closed", "Closed"),
        ],
        default="draft",
        string="State",
        required=True,
        copy=False,
        index=True,
    )

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        for academic_year in self:
            if academic_year.date_start and academic_year.date_end and academic_year.date_start > academic_year.date_end:
                raise ValidationError("The end date must be greater than or equal to the start date.")

    @api.constrains("date_start", "date_end", "active")
    def _check_overlapping_academic_years(self):
        for academic_year in self:
            if not academic_year.active or not academic_year.date_start or not academic_year.date_end:
                continue
            overlapping_years = self.search([
                ("id", "!=", academic_year.id),
                ("active", "=", True),
                ("date_start", "<=", academic_year.date_end),
                ("date_end", ">=", academic_year.date_start),
            ], limit=1)

            if overlapping_years:
                raise ValidationError("The academic year overlaps with another active academic year.")

    @api.depends("date_start", "date_end")
    def _compute_duration_days(self):
        for academic_year in self:
            if academic_year.date_start and academic_year.date_end and academic_year.date_start <= academic_year.date_end:
                academic_year.duration_days = (academic_year.date_end - academic_year.date_start).days + 1
            else:
                academic_year.duration_days = 0

    @api.constrains("is_current", "active", "state")
    def _check_current_academic_year(self):
        for academic_year in self:
            if not academic_year.is_current:
                continue
            if not academic_year.active:
                raise ValidationError("The current academic year must be active.")
            if academic_year.state != "open":
                raise ValidationError("The current academic year must be in the 'open' state.")

            current_years = self.search([
                ("id", "!=", academic_year.id),
                ("is_current", "=", True),
                ("active", "=", True),
            ], limit=1)

            if current_years:
                raise ValidationError("There can be only one current academic year at a time.")

    def action_open(self):
        for academic_year in self:
            if academic_year.state == "closed":
                raise ValidationError("Cannot open a closed academic year.")
            academic_year.state = "open"

    def action_close(self):
        for academic_year in self:
            academic_year.write({
                "state": "closed",
                "is_current": False,
            })

    def action_set_current(self):
        self.ensure_one()
        if not self.active:
            raise ValidationError("Cannot set an inactive academic year as current.")
        if self.state != "open":
            raise ValidationError("Cannot set an academic year as current unless it is in the 'open' state.")
        other_current = self.search([("id", "!=", self.id), ("is_current", "=", True)])
        if other_current:
            other_current.write({"is_current": False})
        self.write({"is_current": True})