# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # city_id = fields.Many2one('res.city.zip', string='Ciudad')
    city_id = fields.Many2one('res.city.zip', string='Ciudad', related='partner_id.zip_id')


    @api.onchange('city_id')
    def onchange_city_id(self):
        for record in self:
            for line in record.order_line:
                line.city_id = record.city_id


    # @api.onchange('order_line')
    # def _onchange_order_line(self):
    #     # super(SaleOrder, self)._onchange_order_line()
    #     for record in self:
    #         for line in record.order_line:
    #             if not line.city_id:
    #                 line.city_id = record.city_id
    



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    city_id = fields.Many2one('res.city.zip', string='Ciudad')
    partner_id = fields.Many2one(readonly=False)

    # @api.onchange('city_id')
    # def onchange_city_id(self):
    #     for record in self:
    #         if record.partner_id.is_ica:
    #             city = record.city_id
    #             taxes_ids = self.env['account.tax'].search([('city_id','=',record.city_id.id),('is_ica','=',True)])
    #             partner_configuration = self.env['res.activity.city.ica'].search([('city_id','=',city.id),('partner_id','=',record.partner_id.id)])
    #             if partner_configuration:
    #                 old_taxes = record.tax_id
    #                 new_taxes = []
    #                 for tax in taxes_ids:
    #                     for conf in partner_configuration:
    #                         if tax.city_id == conf.city_id:
    #                             partner_activity = conf.activity_ids
    #                             for tax_activity in tax.activity_ids:
    #                                 if tax_activity in partner_activity:
    #                                     new_taxes.append(tax.id)
    #                 for tax in old_taxes:
    #                     new_taxes.append(tax.id) if tax not in new_taxes else False
    #                 record.tax_id = new_taxes

    @api.onchange('city_id','partner_id','product_id')
    def onchange_city_id(self):
        for line in self:
            if line.partner_id.is_ica:
                new_taxes = []
                product_taxes = line.product_id.taxes_id
                taxes = line.product_id.taxes_id.ids
                for tax in product_taxes:
                    if tax.is_ica and tax.city_id != line.city_id:
                        new_taxes.append(tax.id)
                if new_taxes:
                    for tax in new_taxes:
                        taxes.remove(tax)
                line.tax_id = taxes
            else:
                taxes = line.product_id.taxes_id
                list = taxes.ids
                for tax in taxes:
                    if tax.is_ica == True:
                        list.remove(tax.id)
                line.tax_id = list


    @api.onchange('product_id')
    def onchange_product_id(self):
        super(PurchaseOrderLine, self).onchange_product_id()
        if not self.partner_id:
            self.partner_id = self.order_id.partner_id.id

