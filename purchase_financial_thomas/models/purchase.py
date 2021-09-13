# -*- coding: utf-8 -*-
#BY: Todoo SAS - LUIS FELIPE PATERNINA VITAL

from odoo import fields,models,api
import re
from odoo.exceptions import ValidationError

class Project_pater(models.Model):
    _inherit = 'purchase.order'
    _description = "Compra"
    
    description_th = fields.Text(string="Observaciones")
    

   
   







    
    
    