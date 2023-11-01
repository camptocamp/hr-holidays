# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2005-2006 Axelor SARL. (http://www.axelor.com)


from odoo import models


class HolidaysAllocation(models.Model):
    """ Allocation Requests Access specifications: similar to leave requests """
    _inherit = "hr.leave.allocation"

    def activity_update(self):
        for manager in self.employee_id.leave_manager_ids:
            old_manager = self.employee_id.leave_manager_id
            self.employee_id.leave_manager_id = manager
            super().activity_update()
            self.employee_id.leave_manager_id = old_manager

    def _check_approval_update(self, state):
        for manager in self.employee_id.leave_manager_ids:
            if manager == self.env.user:
                old_manager = self.employee_id.leave_manager_id
                self.employee_id.leave_manager_id = manager
                super()._check_approval_update(state)
                self.employee_id.leave_manager_id = old_manager
                break
