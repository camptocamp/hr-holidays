# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


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
        for work in res:
            if work.calendar_id.exclude_weekends:
                intervals = res[work]
                new_intervals = []
                for start_int, end_int, attendance in intervals._items:
                    current_dt = start_int
                    while current_dt < end_int:
                        if current_dt.weekday() < 5:
                            next_dt = min(
                                end_int,
                                (current_dt + fields.timedelta(days=1)).replace(
                                    hour=0, minute=0, second=0, microsecond=0
                                ),
                            )
                            new_intervals.append((current_dt, next_dt, attendance))
        return new_intervals
