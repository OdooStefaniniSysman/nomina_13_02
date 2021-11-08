# -*- coding: utf-8 -*-
# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'HR Contract Sena',
    'version': '13.0.1.0.0',
    'category': 'Generic Modules/Human Resources',
    'author': 'todoo',
    'maintainer': 'todoo',
    'company': 'Todoo S.A.S',
    'website': 'https://todoo.co/',
    'depends': [
        'hr_contract',
        'hr_recruitment',
        'hr_payroll_extended',
        'hr_payroll_variations',
        'board',
    ],
    'data': [
        'views/inherited_hr_contract_view.xml',
        'views/hr_contract_sena.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
