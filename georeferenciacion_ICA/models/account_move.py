# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # city_id = fields.Many2one('res.city.zip', string='Ciudad')
    city_id = fields.Many2one('res.city.zip', string='Ciudad', related='partner_id.zip_id')


    @api.onchange('city_id')
    def onchange_city_id(self):
        for line in self.invoice_line_ids:
            line.city_id = self.city_id

    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        super(AccountMove, self)._onchange_invoice_line_ids()
        for record in self:
            for line in record.invoice_line_ids:
                if not line.city_id:
                    line.city_id = record.city_id
    



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    city_id = fields.Many2one('res.city.zip', string='Ciudad')

    # @api.onchange('city_id')
    # def onchange_city_id(self):
    #     for record in self:
    #         if record.partner_id.is_ica:
    #             city = record.city_id
    #             taxes_ids = self.env['account.tax'].search([('city_id','=',city.id),('is_ica','=',True)])
    #             partner_configuration = self.env['res.activity.city.ica'].search([('city_id','=',city.id),('partner_id','=',record.partner_id.id)])
    #             if partner_configuration:
    #                 old_taxes = record.tax_ids
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
    #                 record.tax_ids = new_taxes


    @api.onchange('city_id','product_id')
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
                line.tax_ids = taxes

    
    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     super(AccountMoveLine,self)._onchange_product_id()
    #     if not self.partner_id:
    #         self.partner_id = self.move_id.partner_id