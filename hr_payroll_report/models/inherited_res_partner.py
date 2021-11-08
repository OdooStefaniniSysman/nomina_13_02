# Copyright 2020-TODAY Miguel Pardo <ing.miguel.pardo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    """Add Fields."""
    _inherit = 'res.partner'

    document_type_id = fields.Selection(
        [('NI', 'Número de identificación tributaria'),
         ('CC', 'Cédula de ciudadanía'),
         ('CE', 'Cédula de extranjería'),
         ('TI', 'Tarjeta de identidad'),
         ('PA', 'Pasaporte'),
         ('CD', 'Carné diplomático'),
         ('SC', 'Salvoconducto de permanencia'),
         ('PE', 'Permiso Especial de Permanencia')],
        string="Document Type")
    identification_document = fields.Selection(
        [('PA', 'Pasaporte'),
         ('CD', 'Carne Diplomático'),
         ('TI', 'Tarjeta de Identidad'),
         ('CC', 'Cédula de ciudadanía'),
         ('NI', 'Número de identificacióntributaria'),
         ('SC', 'Salvoconducto de permanencia'),
         ('CE', 'Cédula de Extranjería'),
         ('PE', 'Permiso Especial de Permanencia')],
        string="Document Identification")
    check_digit = fields.Integer()
    contributor_class = fields.Selection(
        [('1', 'Contributor with 200 or more contributors'),
         ('2', 'Contributor with less than 200 contributors'),
         ('3', 'Mipyme contributor that takes advantage of Law 590 of 2000'),
         ('4', 'Beneficiary contributor of article 5 of Law 1429 of 2010'),
         ('5', 'Independent')])
    legal_nature = fields.Selection(
        [('1', 'Pública'),
         ('2', 'Privada'),
         ('3', 'Mixta'),
         ('4', 'Organismos multilaterales'),
         ('5', 'Entidades de derecho público no sometidas a la legislación colombiana')])

    person_pila_type = fields.Selection(
        [('N', 'Natural'),
         ('J', 'Jurídica')])

    ciiu = fields.Many2many('ciiu.value', string="CIIU")

    commercial_register = fields.Char()
    commercial_register_date = fields.Date()
    code_found_layoffs = fields.Char()
    code_compensation_box = fields.Char()
    code_eps = fields.Char()
    code_required_physical_evidence = fields.Char()
    code_unemployee_fund = fields.Char()
    code_arl = fields.Char()
    code_prepaid_medicine = fields.Char()
    code_afc = fields.Char()
    code_afp = fields.Char()
    code_voluntary_contribution = fields.Char()


class CiiuValue(models.Model):
    _name = 'ciiu.value'

    name = fields.Char('Descripción')
    code = fields.Char('Código')
    company_id = fields.Many2one('res.company')
