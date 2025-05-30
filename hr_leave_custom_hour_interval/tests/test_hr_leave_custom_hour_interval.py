from datetime import date

from dateutil.relativedelta import relativedelta

from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestHRLeaveRequest(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create a new employee to avoid conflicts
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "work_email": "test.employee@example.com",
            }
        )

        cls.leave_type = cls.env["hr.leave.type"].create(
            {
                "name": "Legal Leaves",
                "time_type": "leave",
                "requires_allocation": "no",
            }
        )

        first_leave_start = date.today() + relativedelta(days=1)
        first_leave_end = date.today() + relativedelta(days=2)

        cls.first_leave = cls.env["hr.leave"].create(
            {
                "name": "Christmas",
                "employee_id": cls.employee.id,
                "holiday_status_id": cls.leave_type.id,
                "request_date_from": first_leave_start,
                "request_date_to": first_leave_end,
            }
        )

    def test_leave_created_correctly(self):
        self.assertEqual(self.first_leave.name, "Christmas")
        self.assertEqual(self.first_leave.employee_id.id, self.employee.id)
        self.assertEqual(self.first_leave.holiday_status_id.id, self.leave_type.id)
