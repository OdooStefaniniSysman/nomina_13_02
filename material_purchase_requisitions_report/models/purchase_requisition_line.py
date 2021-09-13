# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

class MaterialPurchaseRequisitionLineInherit(models.Model):
    _inherit = "material.purchase.requisition.line"

    ######################################################################################
    total_cost = fields.Integer(string='Costo total', compute = '_compute_cost_total')

    @api.depends('qty','product_id')
    def _compute_cost_total(self):
        for record in self:
            record.total_cost = record.qty * record.product_id.standard_price

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            rec.description = rec.product_id.name
            rec.uom = rec.product_id.uom_id.id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
