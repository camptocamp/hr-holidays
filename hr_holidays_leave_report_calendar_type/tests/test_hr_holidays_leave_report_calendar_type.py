# Copyright 2026 Solvos Consultoría Informática, S.L. (<https://www.solvos.es>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestLeaveReportCalendar(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.leave_type = cls.env["hr.leave.type"].create(
            {
                "name": "Test Holiday Status",
                "requires_allocation": "no",
            }
        )

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee for Leave Report",
            }
        )

        cls.leave = cls.env["hr.leave"].create(
            {
                "name": "Test Leave",
                "employee_id": cls.employee.id,
                "holiday_status_id": cls.leave_type.id,
                "date_from": "2026-04-01 08:00:00",
                "date_to": "2026-04-02 17:00:00",
            }
        )

        cls.leave.action_validate()
        cls.env.flush_all()

    def test_field_exists(self):
        self.assertIn(
            "holiday_status_id",
            self.env["hr.leave.report.calendar"]._fields,
            "holiday_status_id field dont exists.",
        )

    def test_sql_view_column_exists(self):
        self.env.cr.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'hr_leave_report_calendar';
        """
        )
        result = self.env.cr.fetchall()

        column_names = [row[0] for row in result]

        self.assertIn(
            "holiday_status_id",
            column_names,
            "The init() method failed or did not add the holiday_status_id column.",
        )
