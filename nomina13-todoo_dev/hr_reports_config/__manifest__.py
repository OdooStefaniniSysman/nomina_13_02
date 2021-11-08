# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Hr Reports Config',
    'version': '13.0.1.0.0',
    'author': 'Todoo SAS',
    'summary': 'Hr Reports Config for todoo',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'maintainer': 'todoo',
    'company': 'Todoo SAS',
    'website': 'https://todoo.co/',
    'depends': [
        'hr_payroll', 'hr_payroll_variations'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_report_config_data.xml',
        'data/hr_report_config_data_2.xml',
        'data/hr_report_config_data_3.xml',
        'data/hr_pila_report_config_data.xml',
        'views/hr_reports_config_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
