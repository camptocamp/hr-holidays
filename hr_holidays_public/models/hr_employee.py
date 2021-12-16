# Copyright 2021 Camptocamp - Telmo Santos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def list_work_time_per_day(
        self, from_datetime, to_datetime, calendar=None, domain=None
    ):
        return super(
            HrEmployee,
            self.with_context(employee_id=self.id, exclude_public_holidays=True),
        ).list_work_time_per_day(
            from_datetime, to_datetime, calendar=calendar, domain=domain
        )
