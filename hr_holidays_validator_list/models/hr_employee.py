# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    leave_manager_ids = fields.Many2many(
        'res.users',
        string='Time Off',
        compute='_compute_leave_manager',
        store=True,
        readonly=False,
        help='Select the users responsible for approving "Time Off" of this employee.\n'
        'If empty, the approval is done by an Administrator or Approver (determined in settings/users).',
    )

    def create(self, values):
        if ('leave_manager_ids' in values.keys()):
            values['leave_manager_id'] = values['leave_manager_ids'][0][-1][-1]
        res = super().create(values)
        return res

    def write(self, values):
        if ('leave_manager_ids' in values.keys()):
            values['leave_manager_id'] = values['leave_manager_ids'][0][-1][-1]
        res = super().write(values)
        approver_group = self.env.ref('hr_holidays.group_hr_holidays_responsible', raise_if_not_found=False)
        for manager_id in values['leave_manager_ids'][0][-1]:
            if approver_group:
                approver_group.sudo().write({'users': [(4, manager_id)]})
        return res
