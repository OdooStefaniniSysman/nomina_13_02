from odoo import models,fields,api,_

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cost_total = fields.Float('Cost Total', tracking=True)
    quantity = fields.Float('Quantity', tracking=True)
    unit_price = fields.Float('Unit Price', tracking=True)
    price_n_iva = fields.Float('Price Unit without IVA', tracking=True)
    contribution_percentage = fields.Float('Contribution Percentage', tracking=True)

    @api.onchange('partner_id','order_line')
    def onchange_partner_order_line(self):
        if self.partner_id and not self.order_line:
            message = '%s' % self.partner_id.invoice_condition
            mess= {
                'title': _('Invoice Condition!'),
                'message' : message
                  }
            return {'warning': mess}
