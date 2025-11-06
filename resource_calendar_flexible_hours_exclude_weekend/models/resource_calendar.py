# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import fields, models

from odoo.addons.hr_work_entry_contract.models.hr_work_intervals import WorkIntervals


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    exclude_weekends = fields.Boolean()

    # Override to return weekends as special days if exclude_weekends is set
    def _attendance_intervals_batch(
        self, start_dt, end_dt, resources=None, domain=None, tz=None, lunch=False
    ):
        res = super()._attendance_intervals_batch(
            start_dt, end_dt, resources, domain, tz, lunch
        )

        # Filter out weekends from each WorkIntervals
        filtered_results = {}
        # if exclude_weekends AND flexible_hours is True,
        # filter work intervals to remove weekends
        if self.exclude_weekends and self.flexible_hours:
            for resource_id, work_intervals in res.items():
                new_intervals = []
                # Each interval = (start_datetime, end_datetime, attendance_record)
                for start, end, attendance in work_intervals:
                    # Ensure datetime object (not date)
                    start_dt_local = (
                        start
                        if isinstance(start, datetime)
                        else datetime.combine(start, datetime.min.time())
                    )
                    end_dt_local = (
                        end
                        if isinstance(end, datetime)
                        else datetime.combine(end, datetime.min.time())
                    )

                    # Check if start or end is during weekend
                    # weekday(): Monday = 0 ... Sunday = 6
                    if start_dt_local.weekday() in (5, 6) or end_dt_local.weekday() in (
                        5,
                        6,
                    ):
                        continue  # skip weekends
                    new_intervals.append((start, end, attendance))

                # Create new WorkIntervals from filtered data
                filtered_results[resource_id] = WorkIntervals(new_intervals)

            # Return the filtered WorkIntervals per resource
            return filtered_results

        return res
