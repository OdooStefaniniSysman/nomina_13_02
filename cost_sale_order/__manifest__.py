{
    'name': "Cost Sale Order",

    'summary': "Cost Sale Order",

    'description': "Cost Sale Order",

    'author': "Todoo SAS",
    'contributors': "Livingston Arias Narváez la@todoo,co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['contacs_thomas','sale_management','sale_crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
    ],
}
