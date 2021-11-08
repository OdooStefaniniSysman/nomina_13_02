# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError

class MaterialPurchaseRequisitionExt(models.Model):
    _inherit = 'material.purchase.requisition'

    internal_spending = fields.Boolean('Cargar al gasto de consumo interno')
    journal_id = fields.Many2one('account.journal')
    account_move = fields.Many2one('account.move', 'Cuenta ')

    
    def create_assent(self):
        mod = []
        am_obj = self.env['account.move']
        products_no_accounts_internal=[]
        for record in self:

            if record.internal_spending == True:
                
                if record.requisition_line_ids.product_id.categ_id.account_internal_id.id:

                    line = {
                        'name': record.name,
                        'partner_id': record.requisition_line_ids.partner_id.id,
                        'debit': 0.00,
                        'credit': record.requisition_line_ids.total_cost,
                        'account_id': record.requisition_line_ids.product_id.categ_id.account_internal_id.id
                            }
                    mod.append((0,0,line))
                    
                    line = {
                        'name': record.name,
                        'partner_id': record.requisition_line_ids.partner_id.id,
                        'debit': record.requisition_line_ids.total_cost,
                        'credit': 0.00,
                        'account_id': record.requisition_line_ids.product_id.categ_id.property_stock_account_output_categ_id.id
                    }
                    mod.append((0,0,line))

                    if mod:   
                        acc_move_ids = []
                        move = {
                            'journal_id': record.journal_id.id,
                            'line_ids': mod,
                            'date': fields.Date.today(),
                            'ref': record.name ,
                            'type': 'entry'
                        }
                        account_move = am_obj.sudo().create(move)
                        account_move.post()
                        acc_move_ids.append(account_move.id)

                else:
                    products_no_accounts_internal += ''.join(record.name).split(',')

                if products_no_accounts_internal:
                    raise ValidationError("Los siguientes productos deben tener una cuenta de consumo interno: [%s]" % products_no_accounts_internal)

                                    
                
            
    def request_stock(self):

        res = super(MaterialPurchaseRequisitionExt, self).request_stock()

        for record in self:
            record.create_assent()

        return res