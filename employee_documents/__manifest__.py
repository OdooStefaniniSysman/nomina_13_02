# -*- coding: utf-8 -*-
{
    'name': "Employee Documents",

    'summary': """Binder For Storing Employee Documents""",
    'description': """ Unique Binders For Storing Employee Documents""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Employees',
    'version': '13.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'documents', 'hr'],

    # always loaded
    'data': [
        'data/employee_data.xml',
        'views/employee.xml'],
    'post_init_hook': '_assign_binders',
    'uninstall_hook': 'uninstall_hook',
}
