from odoo import api, fields, models

SELECTION_GROUP = [('1 ACTIVOS', '1 ACTIVOS'), ('2 PENSIONADOS', '2 PENSIONADOS'),
                   ('3 JUBILADO ANTICIPADO', '3 JUBILADO ANTICIPADO'), ('4 APRENDICES', '4 APRENDICES'),
                   ('5 RETIRADOS', '5 RETIRADOS'),
                   ('7 TEMPORALES', '7 TEMPORALES'), ('9 EXTERNOS', '9 EXTERNOS'), ]

SELECTION_LABOR = [('01 LEY 50', '01 LEY 50'), ('02 REG ANTERIOR', '02 REG ANTERIOR'), ('03 INTEGRAL', '03 INTEGRAL'),
                   ('04 APRENDIZAJE', '04 APRENDIZAJE'), ('05 PENSIONADO', '05 PENSIONADO'),
                   ('06 EXTERNO/TEMPOR', '06 EXTERNO/TEMPOR')]


class Division(models.Model):
    _name = 'division'
    _description = 'Division'

    name = fields.Char()


class AreaPersonal(models.Model):
    _name = 'area.personal'
    _description = 'AreaPersonal'

    name = fields.Char()


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    division_emp = fields.Many2one('division', 'Division', tracking=True)
    grupo_seleccion_emp = fields.Selection(selection=SELECTION_GROUP, string='Grupo de Personal', tracking=True)
    relacion_laboral_emp = fields.Selection(selection=SELECTION_LABOR, string='Relación Laboral', tracking=True)
    area_personal_emp = fields.Many2one('area.personal', 'Area Personal', tracking=True)
    caja_compensacion_emp = fields.Many2one('res.partner','Caja de compensacion')
