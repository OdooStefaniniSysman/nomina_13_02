# -*- coding: utf-8 -*-
from odoo import models,fields,api,_
import logging

_logger = logging.getLogger(__name__)


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'
    
    bool_prelimit = fields.Boolean('Prelimit')