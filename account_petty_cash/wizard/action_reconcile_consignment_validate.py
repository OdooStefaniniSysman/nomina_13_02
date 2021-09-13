# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentMultiConsignmentValidate(models.TransientModel):
	_name="account.payment.multi.consignment.validate"


	payment_ids = fields.One2many(
		comodel_name='account.payment.multi.consignment.move.validate',
		inverse_name='consignment_id',
		string='Ingresos Afectados',
		required=True,
	)
	
	@api.model
	def default_get(self, fields):
		context = dict(self._context or {})
		active_model = context.get('active_model')
		active_ids = context.get('active_ids')
		payments = self.env[active_model].browse(active_ids)
	
		if any(payment.treasury_move_id.state == 'posted' for payment in payments):
			raise UserError(_("Solo puede validar asientos que no hayan sido validados previamente y este caso esta seleccionando asientos en estado validado"))

		if any(payment.validate_treasury_ok == True for payment in payments):
			raise UserError(_("Solo puede validar asientos que no hayan sido validados previamente"))

		if any(payment.validate_consignation_ok == False or payment.treasury_move_id == False for payment in payments):
			raise UserError(_("Solo puede validar asientos que ya hayan sido consignados previamente"))

		if any(payment.journal_id.type != 'cash' for payment in payments):
			raise UserError(_("Solo puede validar asientos de ingresos en efectivo y en este caso está incluyendo ingresos de banco"))
	
		if any(pay.currency_id != payments[0].currency_id for pay in payments):
			raise UserError(_("Para consignar multiples ingresos a la vez, estos deben tener la misma moneda."))

		rec = {}
		payment_list = []
		total_amount = 0
		journal_cont = 0

		for pay in payments:

			total_amount += pay.amount
			payment_list.append((0,0,{
				'payment_id' : pay.id,
				'journal_id' : pay.journal_id.id,
				'payment_date' : pay.payment_date,
				'partner_id': pay.partner_id.id,
				'name': pay.name,
				'move_id': pay.treasury_move_id.id,
				'amount' : pay.amount,
				}))

		rec.update({'payment_ids':payment_list})
		return rec

	def register_multi_consignment_validate(self):
		if self.payment_ids:
			for payment in self.payment_ids:
				payment_obj = self.env['account.payment'].search([('id','=',payment.payment_id)])
				move_obj = self.env['account.move'].search([('id','=',payment.move_id.id)])
				payment_obj.write({
					'state': 'reconciled',
					'validate_treasury_ok': True,
				})
				move_obj.post()

		else:
			raise UserError(_("Ocurrio un error recuperando los datos de los ingresos, por favor recargue la página e intente realizar el procedimiento nuevamente."))

		return True



class AccountPaymentMultiConsignmentMoveValidate(models.TransientModel):
    _name = 'account.payment.multi.consignment.move.validate'

    consignment_id = fields.Many2one('account.payment.multi.consignment',string='Formulario de Consignación')
    payment_id = fields.Integer(string="ID del Ingreso")
    journal_id = fields.Many2one('account.journal',string='Diario')
    payment_date = fields.Date('Fecha')
    move_id = fields.Many2one('account.move',string='Asiento')
    amount = fields.Float("Total Ingreso", required=False)
    name = fields.Char(string='No. de Ingreso')
    partner_id = fields.Many2one('res.partner',string='Cliente')


