# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import sql

from odoo import fields, models, tools


class LeaveReportCalendar(models.Model):
    _inherit = "hr.leave.report.calendar"

    holiday_status_id = fields.Many2one(
        "hr.leave.type",
        readonly=True,
        string="Time Off Type",
        groups="hr_holidays.group_hr_holidays_user",
    )

    def init(self):
        res = super().init()

        self._cr.execute(
            """
            SELECT view_definition
            FROM information_schema.views
            WHERE table_name = 'hr_leave_report_calendar'
            """
        )
        view_def = self._cr.fetchone()[0]

        if "holiday_status_id" not in view_def:
            view_def = view_def.replace(
                "is_hatched", "is_hatched, hl.holiday_status_id AS holiday_status_id"
            )

            tools.drop_view_if_exists(self._cr, "hr_leave_report_calendar")

            query = sql.SQL(
                "CREATE OR REPLACE VIEW hr_leave_report_calendar AS {}"
            ).format(sql.SQL(view_def))
            self._cr.execute(query)

        return res
