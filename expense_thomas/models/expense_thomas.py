#-*- coding: utf-8 -*-

from odoo import models, fields, api


class ExpenseThomas(models.Model):
    _name = 'expense.thomas'
    _description = 'Thomas expenses'

    name = fields.Char(string='Name')
    request_date = fields.Datetime(string='Request date')
    employee_id = fields.Many2one('hr.employee',string='Technician')
    document = fields.Selection([('money delivery', 'money delivery')
                                ,('money reception','money reception')]
                                , string='Document type')
    coin = fields.Boolean(string='coins')
    bills = fields.Boolean(string='bills')
    refund_date = fields.Datetime(string='refund_date')
    refund_state = fields.Selection([('Pending to return', 'Pending to return')
                                    ,('Returned', 'Returned')], string= "Return state")
    # old coins
    oc_50 = fields.Integer(string='50')
    oc_100 = fields.Integer(string='100')
    oc_200 = fields.Integer(string='200')
    oc_500 = fields.Integer(string='500')
    oc_50_total = fields.Integer(string='total of 50')
    oc_100_total = fields.Integer(string='total of 100')
    oc_200_total = fields.Integer(string='total of 200')
    oc_500_total = fields.Integer(string='total of 500')
    oc_total = fields.Integer(string='total amount old coins')
    #new coins
    nc_50 = fields.Integer(string='50')
    nc_100 = fields.Integer(string='100')
    nc_200 = fields.Integer(string='200')
    nc_500 = fields.Integer(string='500')
    nc_1000 = fields.Integer(string='1000')
    nc_50_total = fields.Integer(string='total of 50')
    nc_100_total = fields.Integer(string='total of 100')
    nc_200_total = fields.Integer(string='total of 200')
    nc_500_total = fields.Integer(string='total of 500')
    nc_1000_total = fields.Integer(string='total of 1000')
    nc_total = fields.Integer(string='total amount new coins')
    #old bills
    ob_1k = fields.Integer(string='1.000')
    ob_2k = fields.Integer(string='2.000')
    ob_5k = fields.Integer(string='5.000')
    ob_10k = fields.Integer(string='10.000')
    ob_20k = fields.Integer(string='20.000')
    ob_50k = fields.Integer(string='50.000')
    ob_1k_total = fields.Integer(string='total of 1.000')
    ob_2k_total = fields.Integer(string='total of 2.000')
    ob_5k_total = fields.Integer(string='total of 5.000')
    ob_10k_total = fields.Integer(string='total of 10.000')
    ob_20k_total = fields.Integer(string='total of 20.000')
    ob_50k_total = fields.Integer(string='total of 50.000')
    ob_total = fields.Integer(string='total amount old bills')
    #new bills
    nb_2k = fields.Integer(string='2.000')
    nb_5k = fields.Integer(string='5.000')
    nb_10k = fields.Integer(string='10.000')
    nb_20k = fields.Integer(string='20.000')
    nb_50k = fields.Integer(string='50.000')
    nb_100k = fields.Integer(string='100.000')
    nb_2k_total = fields.Integer(string='total of 2.000')
    nb_5k_total = fields.Integer(string='total of 5.000')
    nb_10k_total = fields.Integer(string='total of 10.000')
    nb_20k_total = fields.Integer(string='total of 20.000')
    nb_50k_total = fields.Integer(string='total of 50.000')
    nb_100k_total = fields.Integer(string='total of 100.000')
    nb_total = fields.Integer(string='total amount old bills')

    total_coins = fields.Integer(string='total amount coins')
    total_bills = fields.Integer(string='total amount bills')
    total = fields.Integer(string='total amount')

    # old coins
    @api.onchange('oc_50', 'oc_100', 'oc_200', 'oc_500')
    def _onchange_old_coins(self):
        self.oc_50_total = 50*self.oc_50
        self.oc_100_total = 100*self.oc_100
        self.oc_200_total = 200*self.oc_200
        self.oc_500_total = 500*self.oc_500
        self.oc_total = self.oc_50_total + self.oc_100_total + self.oc_200_total + self.oc_500_total
        self.total_coins = self.oc_total + self.nc_total
        self.total = self.total_coins + self.total_bills
        
    
    # new coins
    @api.onchange('nc_50', 'nc_100', 'nc_200', 'nc_500', 'nc_1000')
    def _onchange_new_coins(self):
        self.nc_50_total = 50*self.nc_50
        self.nc_100_total = 100*self.nc_100
        self.nc_200_total = 200*self.nc_200
        self.nc_500_total = 500*self.nc_500
        self.nc_1000_total = 1000*self.nc_1000
        self.nc_total = self.nc_50_total + self.nc_100_total + self.nc_200_total + self.nc_500_total + self.nc_1000_total
        self.total_coins = self.oc_total + self.nc_total
        self.total = self.total_coins + self.total_bills
    
    # old bills
    @api.onchange('ob_1k', 'ob_2k', 'ob_5k', 'ob_10k', 'ob_20k', 'ob_50k')
    def _onchange_old_bills(self):
        self.ob_1k_total = 1000*self.ob_1k
        self.ob_2k_total = 2000*self.ob_2k
        self.ob_5k_total = 5000*self.ob_5k
        self.ob_10k_total = 10000*self.ob_10k
        self.ob_20k_total = 20000*self.ob_20k
        self.ob_50k_total = 50000*self.ob_50k
        self.ob_total = self.ob_1k_total + self.ob_2k_total + self.ob_5k_total + self.ob_10k_total + self.ob_20k_total + self.ob_50k_total
        self.total_bills = self.ob_total + self.nb_total
        self.total = self.total_coins + self.total_bills

    # nw bills
    @api.onchange('nb_2k', 'nb_5k', 'nb_10k', 'nb_20k', 'nb_50k', 'nb_100k')
    def _onchange_new_bills(self):
        self.nb_2k_total = 2000*self.nb_2k
        self.nb_5k_total = 5000*self.nb_5k
        self.nb_10k_total = 10000*self.nb_10k
        self.nb_20k_total = 20000*self.nb_20k
        self.nb_50k_total = 50000*self.nb_50k
        self.nb_100k_total = 100000*self.nb_100k
        self.nb_total = self.nb_100k_total + self.nb_2k_total + self.nb_5k_total + self.nb_10k_total + self.nb_20k_total + self.nb_50k_total
        self.total_bills = self.ob_total + self.nb_total
        self.total = self.total_coins + self.total_bills


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    maintenance_request_ids = fields.Many2many('maintenance.request', string="Maintenance request")
    assigment_thomas_id = fields.Many2one('expense.thomas.assignment',string="expenses assigment thomas")
    partner_id = fields.Many2one('res.partner',string="Proveedor")

    identification_id = fields.Integer(string='N.I.T or C.C.')
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone') 
    city = fields.Char(string='City')
    employee_state = fields.Char(string='State')

    gross_value = fields.Integer(string='Gross value')
    rteiva_rate = fields.Float(string='RETEIVA rate')
    rteiva_value = fields.Float(string='RETEIVA value')
    rtefte_rate = fields.Float(string='RETEFUENTE rate')
    rtefte_value = fields.Float(string='RETEFUENTE value')
    rteica_rate = fields.Float(string='RETEICA rate')
    rteica_value = fields.Float(string='RETEICA value')

    consumption_tax = fields.Float(string='Consumption Tax (value charged on invoice)')
    iva_tax = fields.Float(string='IVA (value charged on invoice)')
    total_pay = fields.Float(string='Total to pay')

    @api.onchange('gross_value','rteiva_rate','rteiva_value','rtefte_rate','rtefte_value','rteica_rate','rteica_value','consumption_tax','iva_tax')
    def onchange_field(self):
        self.rteiva_value = round(self.iva_tax*self.rteiva_rate,0)
        self.rtefte_value = round(self.gross_value*self.rtefte_rate,0)
        self.rteica_value = round((self.gross_value*self.rteica_rate)/1000,0)
        self.total_pay = self.gross_value + self.iva_tax - self.rteiva_value - self.rtefte_value - self.rteica_value + self.consumption_tax
    
    
class ExpenseThomasAssignment(models.Model):
    _name = 'expense.thomas.assignment'
    _description = 'Thomas expenses assignment'

    def _compute_expenses_ids(self):
        for record in self:
            record.hr_expense_ids = self.env["hr.expense"].search([('employee_id', '=', self.employee_id.id)
                                                                ,('date', '<=', self.end_date)
                                                                ,('date', '>=', self.initial_date)
                                                                ,'|',('state', '=', 'reported')
                                                                ,'|',('state', '=', 'approved')
                                                                ,('state', '=', 'done')])
            total=0
            for line in record.hr_expense_ids:
                total += line.total_amount
            record.total_residual = record.advance - total


    state = fields.Selection([('assign', 'assign')
                                ,('approve','approve')
                                ,('rejected','rejected')
                                ,('close','close')]
                                , string='State'
                                ,default='assign')
    #Advance
    name = fields.Char(string='Name')
    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string='Product')
    advance = fields.Integer(string="Advance value")
    advance_date = fields.Date(string="Advance date")
    employee_id = fields.Many2one('hr.employee', string='Technician')
    # identification = fields.Char(string='Identification')
    # exp_place = fields.Char(string="Expedition place")
    initial_date = fields.Date(string="Start date")
    end_date = fields.Date(string="End date")
    total_residual = fields.Float(striing='Advance residual', compute='_compute_expenses_ids')
    identification_id = fields.Char(string='Identification', related='employee_id.identification_id')
    bank_account_id = fields.Many2one('res.partner.bank',string='Bank Account Number', related='employee_id.bank_account_id')
    bank_id = fields.Many2one('res.bank',string='Bank', related='employee_id.bank_account_id.bank_id')
    city = fields.Char(string='City')

    #Totals
    total_by_payroll = fields.Integer(string='Total by payroll')
    discount = fields.Integer(string='Discount')
    total_discount = fields.Integer(string='Total payroll with discount')
    total_transport = fields.Integer(string='Total transport', related='advance')
    total_required = fields.Integer(string='Total required')

    #hotel
    hotel_days = fields.Integer(string='Days in hotel')
    unitary_hotel = fields.Integer(string='Hotel unit value')
    total_hotel = fields.Integer(string='Total hotel value')

    unpaid_hotel_days = fields.Integer(string='Unpaid hotel days')
    unpaid_unitary_hotel = fields.Integer(string='Unpaid hotel unitary value')
    unpaid_total_hotel = fields.Integer(string='Unpaid total hotel value')

    total_hotel_days = fields.Integer(string='Total pay and unpaid') 

    #Food
    feeding_days = fields.Integer(string='Feeding days') 
    unit_value_feeding = fields.Integer(string='Unitary value of feeding days') 
    total_feeding_value = fields.Integer(string='Total feeding value')

    unpaid_feeding_days = fields.Integer(string='Unpaid feeding days') 
    unpaid_unit_value_feeding = fields.Integer(string='Unitary value of unpaid feeding days') 
    unpaid_total_feeding = fields.Integer(string='Total unpaid feeding days')
    total_feeding = fields.Integer(string='Total paid and unpaid feeding days')


    made_by = fields.Binary(string="Made by")
    reviewed_by = fields.Binary(string="Reviewed by")
    approved_by = fields.Binary(string="Approved by")
    managment_sign = fields.Binary(string="Approved by financial management") 

    hr_expense_ids = fields.One2many('hr.expense', 'assigment_thomas_id', string='Expenses', compute='_compute_expenses_ids')

    @api.onchange('hotel_days','unitary_hotel','unpaid_hotel_days','unpaid_unitary_hotel','feeding_days',
                                    'unit_value_feeding','unpaid_feeding_days','unpaid_unit_value_feeding')
    
    def onchange_hotel(self):
        self.total_hotel = self.hotel_days*self.unitary_hotel
        self.unpaid_total_hotel = self.unpaid_hotel_days*self.unpaid_unitary_hotel
        self.total_hotel_days = self.total_hotel + self.unpaid_total_hotel
        self.total_feeding_value = self.feeding_days*self.unit_value_feeding
        self.unpaid_total_feeding = self.unpaid_feeding_days*self.unpaid_unit_value_feeding
        self.total_feeding = self.total_feeding_value + self.unpaid_total_feeding
        self.total_by_payroll = self.total_hotel_days + self.total_feeding
        self.discount = self.total_by_payroll*0.08
        self.total_discount = self.total_by_payroll-self.discount
        self.total_required = self.total_transport + self.total_by_payroll


    def get_sign_made_by(self):
        self.made_by = self.env.user.sign_signature

    def get_sign_reviewed_by(self):
        self.reviewed_by = self.env.user.sign_signature

    def get_sign_approved_by(self):
        self.approved_by = self.env.user.sign_signature

    def get_sign_managment_by(self):
        self.managment_sign = self.env.user.sign_signature