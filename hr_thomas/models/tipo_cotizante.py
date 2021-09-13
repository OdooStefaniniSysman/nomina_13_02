from odoo import fields,models,api



class Todoo_tipo_cotizante(models.Model):
    _name = 'tipo.cotizante'
    _rec_name = 'nombre_tipo_cotizante'
   
    nombre_tipo_cotizante=fields.Char()
    code = fields.Char()
    has_arl = fields.Boolean()
    has_afp = fields.Boolean()
    has_eps = fields.Boolean()
    has_ccf = fields.Boolean()
    eps_rate = fields.Float()
    pension_rate = fields.Float()
    eps_rate = fields.Float()
    ccf_rate = fields.Float()
    arl_rate = fields.Float()
    



