# -*- coding: utf-8 -*-

{
    'name': 'HR Payroll Account Extended',
    'summary': 'HR Payroll Account Customization for todoo',
    'version': '13.0.1.0.1',
    'category': 'Human Resources',
    'website': 'https://todoo.co/',
    'author': 'Todoo S.A.S',
    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'hr_payroll_account',
    ],
    'data': [
        'view/hr_salary_rule_view.xml',
    ],
}
