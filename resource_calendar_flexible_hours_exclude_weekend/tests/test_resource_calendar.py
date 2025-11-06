from datetime import datetime

import pytz

from odoo.tests.common import TransactionCase


class TestResourceCalendar(TransactionCase):
    def test_flexible_calendar_attendance_interval_duration_exclude_weekends(self):
        """
        Test that the duration of an attendance interval for
        flexible calendar is correctly computed.
        """
        calendar = self.env["resource.calendar"].create(
            {
                "name": "Flexible Calendar",
                "hours_per_day": 8.0,
                "full_time_required_hours": 40.0,
                "flexible_hours": True,
                "exclude_weekends": True,
            }
        )
        UTC = pytz.timezone("UTC")
        start_dt = datetime(2025, 6, 4, 0, 0, 0).astimezone(UTC)
        end_dt = datetime(2025, 6, 4, 12, 0, 0).astimezone(UTC)
        result_per_resource_id = calendar._attendance_intervals_batch(start_dt, end_dt)
        start, end, _ = result_per_resource_id[0]._items[0]

        actual_duration = end - start

        self.assertEqual(
            actual_duration.seconds / 3600,
            calendar.full_time_required_hours,
            "For a full day, the interval must match full time required hours",
        )
