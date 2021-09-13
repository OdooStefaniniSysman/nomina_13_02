{
    'name': 'Hr Employee Substitution',
    'version': '13.0.1.0.0',
    'summary': 'Employer Substitution',
    'description': 'Employer substitution for an employee of a company',
    'category': 'Human Resources',
    'website': 'https://todoo.co/',
    'author': 'todoo',
    'depends': ['base', 'hr_management_human_talent', 'hr_payroll_variations', 'hr_payroll_dis_aid'],
    'demo': [''],
    'data': [
            #'security/ir.model.access.csv',
             'data/hr_employee_substitution_data.xml',
             'views/hr_employee_substitution_views.xml',
             #'views/new_fields_todoo_views.xml',
             'views/menu_items_views.xml',
             ],
}
