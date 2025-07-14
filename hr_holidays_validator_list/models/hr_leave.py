# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class HolidaysLeave(models.Model):
    """Allocation Requests Access specifications: similar to leave requests"""

    _inherit = "hr.leave"

    def _get_responsible_for_approval(self):
        self.ensure_one()

        if self.validation_type == "manager" or (
            self.validation_type == "both" and self.state == "confirm"
        ):
            if self.employee_id.leave_manager_ids:
                return self.employee_id.leave_manager_ids

        return super()._get_responsible_for_approval()
