# Copyright 2020-2025 Tecnativa - Víctor Martínez
# Copyright 2024 Tecnativa - Carlos Lopez
# Copyright 2025 Grupo Isonor - Alexandre D. Díaz
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from collections import defaultdict

from odoo import models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _get_durations(self, check_leave_type=True, resource_calendar=None):
        # We need to set request_unit as 'day'
        # to avoid the calculations being done as hours.
        mod_holidays_status_ids = self.env.context.get("mod_holidays_status_ids", [])
        natural_day_instances = self.filtered(
            lambda x: x.holiday_status_id.id in mod_holidays_status_ids
            or x.holiday_status_id.request_unit
            in ("natural_day", "natural_day_half_day")
        )
        orig_status_request_units = {
            leave.holiday_status_id.id: leave.holiday_status_id.request_unit
            for leave in self
        }

        for natural_day in natural_day_instances:
            orig_request_unit = orig_status_request_units[
                natural_day.holiday_status_id.id
            ]
            natural_day.holiday_status_id.sudo().request_unit = (
                "half_day" if orig_request_unit == "natural_day_half_day" else "day"
            )

        _self = self - natural_day_instances
        leaves_by_orig_ru = defaultdict(lambda: self.env["hr.leave"])
        for leave in _self:
            orig_request_unit = orig_status_request_units[leave.holiday_status_id.id]
            leaves_by_orig_ru[orig_request_unit] += leave

        res = defaultdict(list)
        for orig_request_unit, leaves in leaves_by_orig_ru.items():
            _leaves = leaves.with_context(old_request_unit=orig_request_unit)
            subres = super(HrLeave, _leaves)._get_durations(
                check_leave_type=check_leave_type, resource_calendar=resource_calendar
            )
            for k, v in subres.items():
                res[k].extend(v)

        if not natural_day_instances:
            return res
        _res = super(
            HrLeave, natural_day_instances.with_context(natural_period=True)
        )._get_durations(
            check_leave_type=check_leave_type, resource_calendar=resource_calendar
        )
        for item in natural_day_instances:
            res[item.id] = _res[item.id]

        for natural_day in natural_day_instances:
            orig_request_unit = orig_status_request_units[
                natural_day.holiday_status_id.id
            ]
            natural_day.holiday_status_id.sudo().request_unit = orig_request_unit

        return res
