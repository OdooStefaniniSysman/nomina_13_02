# -*- coding: utf-8 -*-
# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Payslip Settlement',
    'version': '12.0.1.0.0',
    'summary': """ """,
    'sequence': 15,
    'category': 'Human Resources',
    'author': 'Todoo S.A.S',
    'license': 'AGPL-3',
    'maintainer': 'Todoo',
    'company': 'Todoo S.A.S',
    'website': 'https://todoo.co/',
    'description': """
    """,
    'depends': ['hr_payroll', 'hr_payroll_variations'],
    'data': [
        'security/ir.model.access.csv',
        'views/type_settlement_view.xml',
        'views/assign_month_view.xml',
        'views/inherited_hr_payslip_view.xml'
    ],
    'installable': True,
    'application': True,
}
