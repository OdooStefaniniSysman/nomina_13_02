# -*- coding: utf-8 -*-
#BY: ING.LUIS FELIPE PATERNINA VITAL - TODOO SAS.

from odoo import fields,models,api



class Todoo(models.Model):
  _inherit = 'res.partner'

  identificador = fields.Char('Identificador')
  tipo = fields.Selection([('AFP', 'AFP'),('AFC', 'AFC'),('ARL','ARL'),('EPS','EPS'),('CAJA DE COMPENSACIÓN','CAJA DE COMPENSACIÓN')],tracking=True, string="Clasificación UGPP")
  check_arl = fields.Boolean(string="ARL")
  identificator_arl = fields.Char(string="Identificador ARL")
  check_afp = fields.Boolean(string="AFP")
  identificator_afp = fields.Char(string="Identificador AFP")
  check_box = fields.Boolean(string="Caja de Compensación")
  identificator_box = fields.Char(string="Identificador Caja de Compensación")
  check_eps = fields.Boolean(string="EPS")
  identificator_eps = fields.Char(string="Identificador EPS")
  check_afc = fields.Boolean(string="AFC")
  identificator_afc = fields.Char(string="Identificador AFC")
  check_court = fields.Boolean(string="Juzgado")
  identificator_court = fields.Char()
  check_loan = fields.Boolean(string="Descuentos")
  check_colombia_form=fields.Boolean('Seleccion Colombia', compute='_compute_check_country_id')

  @api.depends('country_id')
  def _compute_check_country_id(self):
    for record in self:
      record.check_colombia_form = True if record.country_id and record.country_id[0].name  == 'Colombia' else False

