
#LUIS FELIPE PATERNINA VITAL - TODOO SAS
from odoo import api, fields, models



class HrDepartureWizard(models.TransientModel):
    _inherit = "hr.departure.wizard"
    
    departure_reason = fields.Selection(selection_add=[
        ('mutuo acuerdo', 'Mutuo Acuerdo'),
        ('expiracion plazo fijo pactado', 'Expiración plazo fijo pactado'),
        ('terminacion de la obra o labor', 'Terminación de la obra o labor'),
        ('retiro con justa causa','Retiro con justa causa'),
        ('retiro sin justa causa','Retiro sin justa causa'),
        ('invalidez total para trabajar','Invalidez total para trabajar'),
        ('muerte del trabajador','Muerte del trabajador'),
        ('liquidacion o clausura empresa','Liquidación o clausura empresa'),
        ('jubilacion por vejez','Jubilación por vejez'),
        ('terminacion cont.aprendizaje','Terminación Cont. Aprendizaje'),
        ('terminacion periodo prueba','Terminación Período Prueba'),
        ('renuncia','Renuncia'),
    ], string="Motivo de salida")

    fecha_retiro = fields.Date(string="Fecha de Retiro")
    plan_id = fields.Many2one('hr.plan', default=lambda self: self.env['hr.plan'].search([], limit=1))

    def action_register_departure(self):
        res = super(HrDepartureWizard,self).action_register_departure()
        employee = self.employee_id
        employee.fourth_name = employee.fourth_name + ' ARCHIVADO'
        employee.name = employee.name + ' ARCHIVADO'
        employee.fecha_retiro = self.fecha_retiro
        return res
