# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleMultiCustomer(models.Model):
    _name = 'sale.multi.customer'

    sale_id = fields.Many2one('sale.order', string='Pedido de Venta')
    percent = fields.Float(string='Porcentaje (%)') #, digits=(2,2)
    partner_id = fields.Many2one('res.partner', string='Cliente')

    def unlink(self):
        for record in self:
            if record.sale_id.partner_id.id == record.partner_id.id:
                raise ValidationError(_('No pude elimiar el adquiriente que está seleccionado en el campo cliente'))
        return super(SaleMultiCustomer, self).unlink()
    
    