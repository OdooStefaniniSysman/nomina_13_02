
{
    'name': 'Reporte Módulo de requisiciones',
    'version': '1.7.2',
    'price': 79.0,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'summary': """This module allow your employees/users to create Purchase Requisitions.""",
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'http://www.probuse.com',
    'support': 'contact@probuse.com',
    'category': 'Warehouse',
    'depends': [
                'material_purchase_requisitions',
                'stock',
                'product',
                'account',
                ],
    'data':[
                'report/purchase_requisition_template.xml',
                'views/purchase_requisition_view.xml',
                'views/purchase_requisition_report.xml',
                'views/product_category_view.xml',
                ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
