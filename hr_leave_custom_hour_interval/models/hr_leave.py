# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    request_time_hour_from = fields.Float("Float hour from")
    request_time_hour_to = fields.Float("Float hour to")

    request_hour_from_display = fields.Char(
        compute="_compute_hour_from_display", store=True
    )
    request_hour_to_display = fields.Char(
        compute="_compute_hour_to_display", store=True
    )

    @api.depends("request_time_hour_from")
    def _compute_hour_from_display(self):
        for leave in self:
            leave.request_hour_from_display = (
                f"{leave.request_time_hour_from:.2f}"
                if leave.request_time_hour_from is not None
                else ""
            )

    @api.depends("request_time_hour_to")
    def _compute_hour_to_display(self):
        for leave in self:
            leave.request_hour_to_display = (
                f"{leave.request_time_hour_to:.2f}"
                if leave.request_time_hour_to is not None
                else ""
            )
