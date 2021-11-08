# -*- coding: utf-8 -*-
from itertools import groupby

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def create(self):
        raise UserError(_('You can not create record in production environment.'))

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def create(self):
        raise UserError(_('You can not create record in production environment.'))


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create(self):
        raise UserError(_('You can not create record in production environment.'))


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def create(self):
        raise UserError(_('You can not create record in production environment.'))

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def create(self):
        raise UserError(_('You can not create record in production environment.'))

class MaterialPurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    def create(self):
        raise UserError(_('You can not create record in production environment.'))

