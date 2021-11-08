import logging

from odoo import api, fields, models, tools

from odoo.addons.base.models.ir_config_parameter import (
    IrConfigParameter as IrConfigParameterOriginal,
)

_logger = logging.getLogger(__name__)

# params that has to be shared across all companies
SHARED_KEYS = ["database.expiration_date"]
FIELD_NAME = "value"

class MailAlias(models.Model):
    _inherit = 'mail.alias'

    alias_domain = fields.Char('Alias domain',
    readonly=False,
    store=True
    )