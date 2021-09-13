# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_multi_customer = fields.Boolean(string="Multiples adquirientes?", default=False, copy=True)
    multi_customer_ids = fields.One2many('sale.multi.customer', 'sale_id', string='Adquirientes', copy=True)

    def action_confirm(self):
        for record in self:
            if record.is_multi_customer:
                if sum([x.percent for x in record.multi_customer_ids]) != 100.0:
                    raise ValidationError(_('El porcentaje de participación de los adquirientes no completa el 100% del pedido'))
                if record.multi_customer_ids.filtered(lambda x: x.percent <= 0.0):
                    raise ValidationError(_('No pueden haber adquirientes con porcentajes de participación nulos o negativos'))
        return super(SaleOrder, self).action_confirm()

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        customers = []
        if self.is_multi_customer:
            for customer in self.multi_customer_ids:

                customers.append((0,0,{
                    'partner_id': customer.partner_id.id,
                    'percent': customer.percent,
                }))
        res.update({
            'is_multi_customer': self.is_multi_customer,
            'multi_customer_ids': customers,
        })
        return res

    @api.onchange('partner_id', 'is_multi_customer')
    def _onchange_partner_id_multi_customer(self):
        if self.is_multi_customer:
            if self.partner_id:
                self.multi_customer_ids = False
                self.multi_customer_ids = [(0,0,{
                    'partner_id': self.partner_id.id,
                    'sale_id': self.id,
                })]
        else:
            self.multi_customer_ids = False
    
    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        if res.is_multi_customer and res.partner_id.id not in res.multi_customer_ids.mapped('partner_id').ids:
            raise ValidationError(_('El cliente debe aparecer en la tabla de adquirientes.'))
        return res
    
    def write(self, vals):
        # Add code here
        res = super(SaleOrder, self).write(vals)
        for record in self:
            if record.is_multi_customer and record.partner_id.id not in record.multi_customer_ids.mapped('partner_id').ids:
                raise ValidationError(_('El cliente debe aparecer en la tabla de adquirientes.'))
        return res
    
    