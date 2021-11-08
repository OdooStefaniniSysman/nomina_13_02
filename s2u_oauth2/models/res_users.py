# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models
from datetime import datetime
from urllib.parse import urlparse
import json

import logging
logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    office365_access_token = fields.Char("Access Token")
    office365_refresh_token = fields.Char("Refresh Token")
    office365_expiration = fields.Datetime("End time")
