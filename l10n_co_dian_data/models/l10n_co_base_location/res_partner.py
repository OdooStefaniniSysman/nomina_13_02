# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    zip_id = fields.Many2one("res.city.zip", "ZIP Location")
    country_code = fields.Char(related='country_id.code', store=False)

    def update_all_location(self):
        partner_ids = self.search([]).filtered(lambda x: x.city_crm and not x.city_id)
        for partner in partner_ids:
            partner.update_self_location()

    def update_self_location(self):
        self.ensure_one()
        if self.city_crm:
            city_id = self.city_crm
            zip_id = self.env['res.city.zip'].search([('city_id','=',city_id.id)], limit=1)
            if zip_id and self.state_id and zip_id.city_id.state_id.id != self.state_id.id:
                city_id = self.env['res.city'].search([('name','=',city_id.name),('state_id','=',self.state_id.id)], limit=1)
                if city_id:
                    zip_id = self.env['res.city.zip'].search([('city_id','=',city_id.id)], limit=1)
                else:
                    zip_id = False
            if zip_id:
                self.zip_id = zip_id.id
                self._onchange_zip_id()
                _logger.info('ZIP - ' + str(self.city_id.name))
            else:
                self.city_id = city_id.id
                self.state_id = city_id.state_id.id or False
                self.country_id = city_id.country_id.id or False
                _logger.info('City - ' + str(self.city_id.name))

    @api.onchange("city_id")
    def _onchange_city_id(self):
        if not self.zip_id:
            super()._onchange_city_id()
        if self.zip_id and self.city_id != self.zip_id.city_id:
            self.update({"zip_id": False, "zip": False, "city": False})
        if self.city_id and self.country_enforce_cities:
            return {"domain": {"zip_id": [("city_id", "=", self.city_id.id)]}}
        return {"domain": {"zip_id": []}}

    @api.onchange("country_id")
    def _onchange_country_id(self):
        res = super()._onchange_country_id()
        if self.zip_id and self.zip_id.city_id.country_id != self.country_id:
            self.zip_id = False
        return res

    @api.onchange("zip_id")
    def _onchange_zip_id(self):
        if self.zip_id:
            vals = {
                "city_id": self.zip_id.city_id,
                "zip": self.zip_id.name,
                "city": self.zip_id.city_id.name,
            }
            if self.zip_id.city_id.country_id:
                vals.update({"country_id": self.zip_id.city_id.country_id})
            if self.zip_id.city_id.state_id:
                vals.update({"state_id": self.zip_id.city_id.state_id})
            self.update(vals)
        elif not self.country_enforce_cities:
            self.city_id = False

    @api.constrains("zip_id", "country_id", "city_id", "state_id")
    def _check_zip(self):
        if self.env.context.get("skip_check_zip"):
            return
        for rec in self:
            if not rec.zip_id:
                continue
            if rec.state_id and rec.zip_id.city_id.state_id != rec.state_id:
                raise ValidationError(
                    _("The state of the partner %s differs from that in " "location %s")
                    % (rec.name, rec.zip_id.name)
                )
            if rec.country_id and rec.zip_id.city_id.country_id != rec.country_id:
                raise ValidationError(
                    _(
                        "The country of the partner %s differs from that in "
                        "location %s"
                    )
                    % (rec.name, rec.zip_id.name)
                )
            if rec.city_id and rec.type != 'contact' and rec.zip_id.city_id != rec.city_id:
                raise ValidationError(
                    _("The city of partner %s differs from that in " "location %s")
                    % (rec.name, rec.zip_id.name)
                )

    @api.onchange("state_id")
    def _onchange_state_id(self):
        vals = {}
        if self.state_id.country_id:
            vals.update({"country_id": self.state_id.country_id})
        if self.zip_id and self.state_id != self.zip_id.city_id.state_id:
            vals.update({"zip_id": False, "zip": False, "city": False})
        self.update(vals)
        if self.state_id and not self.zip_id:
            cities_ids = self.env['res.city'].search([('state_id','=',self.state_id.id)]).ids
            return {'domain': {'zip_id': [('city_id', 'in', cities_ids)],
                               'city_id': [('id', 'in', cities_ids)]}}
