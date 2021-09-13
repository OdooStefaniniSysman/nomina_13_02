# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentMultiConsignment(models.TransientModel):
	_name="account.payment.multi.consignment"

	memo = fields.Char(string='Observaciones')
	journal_id = fields.Many2one('account.journal',string='Banco donde Consigna',domain=[('type', '=', 'bank')],required=True)
	payment_ids = fields.One2many(
		comodel_name='account.payment.multi.consignment.payment',
		inverse_name='consignment_id',
		string='Ingresos Afectados',
		required=True,
	)
	currency_id = fields.Many2one('res.currency', string="Moneda de la Compañia", related='journal_id.company_id.currency_id', readonly=True)
	partner_id = fields.Many2one('res.partner',string='Tercero', related='journal_id.partner_id', readonly=True,required=True)
	amount_total = fields.Monetary(string='Total Consignado')
	date = fields.Date('Fecha de la Consignación',required=True, default=datetime.today())
	journal_payment_id = fields.Many2one('account.journal',string='Origen de la Consignación',domain=[('type', '=', 'cash')],required=True, readonly=True)
	account_analytic_tag_id = fields.Many2one('account.analytic.tag',string='Etiqueta Analítica', readonly=True)
	consignment_file = fields.Binary(
        string='Soporte de Consignación',
    )

	session_id = fields.Many2one(
        'treasury.session', 
        string='Sesión', 
        required=True,
        domain="[('state', '=', 'opened')]")

	def _compute_amount_base_payment(self):
		self.amount_base = 0.0
		payment_data = self.env['account.payment'].search([('id','ind',self.payment_ids),('state','=','posted')])
		for payment in payment_data:
			self.amount_base += payment.amount
		
	def _get_payments(self):
		return self.env['account.payment'].browse(self._context.get('active_ids',[]))

	@api.onchange('journal_id')
	def _onchange_journal_id(self):
		if not self.journal_id.partner_id and self.journal_id:
			raise UserError(_("El diario seleccionado debe tener un tercero asociado"))

		self.amount_total = 0.0
		for payment in self.payment_ids:
			self.amount_total += payment.amount_consignment

	@api.model
	def default_get(self, fields):
		context = dict(self._context or {})
		active_model = context.get('active_model')
		active_ids = context.get('active_ids')
		payments = self.env[active_model].browse(active_ids)
	
		if any(payment.state != 'posted' for payment in payments):
			raise UserError(_("Solo puede consignar ingresos en estado validado"))

		if any(payment.validate_consignation_ok == True for payment in payments):
			raise UserError(_("Solo puede consignar ingresos que no hayan sido consignados anteriormente"))

		if any(payment.journal_id.type != 'cash' for payment in payments):
			raise UserError(_("Solo puede consignar ingresos en efectivo y en este caso está incluyendo ingresos de banco"))
	
		if any(pay.currency_id != payments[0].currency_id for pay in payments):
			raise UserError(_("Para consignar multiples ingresos a la vez, estos deben tener la misma moneda."))

		rec = {}
		payment_list = []
		total_amount = 0
		journal_cont = 0
		journal_payment_id = None
		account_analytic_tag_id = None
		for pay in payments:
			if journal_payment_id != pay.journal_id.id and journal_payment_id:
				journal_payment_id = pay.journal_id.id
				journal_cont+=1
			if not journal_payment_id:
				journal_payment_id = pay.journal_id.id
			total_amount += pay.amount
			payment_list.append((0,0,{
				'payment_id' : pay.id,
				'amount' : pay.amount,
				'amount_consignment' : pay.amount,
				'journal_id' : pay.journal_id.id,
				'payment_date' : pay.payment_date,
				'payment_account_id' : pay.journal_id.default_credit_account_id.id,
				'partner_id': pay.partner_id.id,
				'name': pay.name,
				}))
			if not pay.session_id.config_id.account_analytic_tag_id.id:
				raise UserError(_("El punto de venta asociado a este método de pago no tiene definido una cuenta analítica."))
			else:
				account_analytic_tag_id = pay.session_id.config_id.account_analytic_tag_id.id

		if journal_cont > 0:
			raise UserError(_("Lo ingresos seleccionados deben ser del mismo Diario o Método de Pago"))
		rec.update({'payment_ids':payment_list})
		rec.update({
			'partner_id': self.journal_id.partner_id.id,
			'amount_total': total_amount,
			'journal_payment_id': journal_payment_id,
		})
		if account_analytic_tag_id:
			rec.update({
				'account_analytic_tag_id': account_analytic_tag_id,
			})


		team_ids = self.env['crm.team'].search([('member_ids', '=', self.env.uid)])
		for team in team_ids:
			config_obj = self.env['treasury.config'].search([('crm_team_id', '=', team.id)], limit=1)
			session_obj = self.env['treasury.session'].search([('config_id', '=', config_obj.id),('state','=','opened')], limit=1)
			if session_obj.id:
				rec.update({
					'session_id': session_obj.id,
				})
		return rec

	def register_multi_consignment(self):
		if self.payment_ids:
			account_move = self.env['account.move']
			ctx = dict(self._context, lang=self.partner_id.lang)
			move_lines = []
			account_reconcile_id = self.journal_id.default_debit_account_id
			total_amount = 0.0
			for payment in self.payment_ids:
				total_amount += payment.amount
				payment_obj = self.env['account.payment'].search([('id','=',payment.payment_id)])

				account_payment_id = self.env['account.payment'].search([('id','=',payment.payment_id)]).journal_id.default_debit_account_id
				move_lines.append({
                    'name': str(payment.name),
                    'debit': 0.0, 
                    'credit': payment.amount,
                    'account_id': account_payment_id.id,
                    'date': self.date,
                    'partner_id': payment.partner_id.id,
                    'quantity': 1,
	                'amount_currency': 0.0,
                    'currency_id': False,
                    'analytic_tag_ids': [(4, self.account_analytic_tag_id.id)]
                    #'payment_id': payment.payment_id,
                })
				

			move_lines.append({
                'name': 'Conciliación Bancaria',
                'debit': total_amount, 
                'credit': 0.0,
                'account_id': account_reconcile_id.id,
                'date': self.date,
                'partner_id': self.partner_id.id,
                'quantity': 1,
                'amount_currency': 0.0,
                'currency_id': False,
                'analytic_tag_ids': [(4, self.account_analytic_tag_id.id)]
            })
			move_vals = {
				'ref': 'Conciliación Bancaria: ' + str(self.memo),
                'journal_id': self.journal_id.id,
                'date': self.date,
                'name': '/',
			}

			move = self.env['account.move'].with_context(default_journal_id=move_vals['journal_id']).create(move_vals)
			move.write({'line_ids': [(0, 0, line) for line in move_lines]})
			for payment in self.payment_ids:
				payment_obj = self.env['account.payment'].search([('id','=',payment.payment_id)])
				payment_obj.write({
					'validate_consignation_ok': True,
					'treasury_move_id': move.id,
					'consignment_file': self.consignment_file
				})

			#session_obj = self.env['treasury.session'].search([('id','=',self.session_id)])
			self.session_id.cash_register_consigned += total_amount

		else:
			raise UserError(_("Ocurrio un error recuperando los datos de los ingresos, por favor recargue la página e intente realizar el procedimiento nuevamente."))

		return True



class AccountPaymentMultiConsignmentLine(models.TransientModel):
    _name = 'account.payment.multi.consignment.payment'

    consignment_id = fields.Many2one('account.payment.multi.consignment',string='Formulario de Consignación')
    payment_id = fields.Integer(string="ID del Ingreso")
    amount = fields.Float("Valor Ingreso", required=False)
    amount_consignment = fields.Float("Valor Consignado", required=True)
    journal_id = fields.Many2one('account.journal',string='Diario')
    payment_account_id = fields.Many2one('account.account',string='Cuenta')
    payment_date = fields.Date('Fecha')
    name = fields.Char(string='No. de Ingreso')
    partner_id = fields.Many2one('res.partner',string='Cliente')

