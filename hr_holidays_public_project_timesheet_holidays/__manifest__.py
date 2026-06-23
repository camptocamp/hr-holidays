# Copyright 2015 2011,2013 Michael Telahun Makonnen <mmakonnen@gmail.com>
# Copyright 2020 InitOS Gmbh
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "HR Holidays Public Project Timesheet",
    "version": "19.0.1.0.0",
    "license": "AGPL-3",
    "category": "Human Resources",
    "author": "Camptocamp SA, Odoo Community Association (OCA),",
    "summary": "Manage Timesheets forPublic Holidays",
    "website": "https://github.com/OCA/hr-holidays",
    "depends": [
        "hr_holidays_public",
        "project_timesheet_holidays",
    ],
    "data": [],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "auto_install": True,
}
