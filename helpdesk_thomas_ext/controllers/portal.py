# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.osv.expression import OR


class CustomerPortalHelpdesk(CustomerPortal):

    @http.route([ 
        "/helpdesk/ticket/reject/<int:ticket_id>"
        
    ], type='http', auth="public", website=True)
    def tickets_followup_rechazar(self, ticket_id=None, access_token=None, **kw):
        try:
            ticket_sudo = self._document_check_access('helpdesk.ticket', ticket_id, access_token)
            team_id = request.env['helpdesk.ticket'].sudo().search([('id','=',ticket_id)])
            if team_id.team_label == 'MESA DE AYUDA TECNOLOGÍA':
                ticket_stage = ticket_sudo.stage_id.search([('name','=','EN REVISIÓN')])
            elif team_id.team_label == 'MESA DE AYUDA SEGURIDAD':
                ticket_stage = ticket_sudo.stage_id.search([('name','=','REVISIÓN')])

            ticket_sudo.write({'stage_id':ticket_stage.id})

        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._ticket_get_page_view_values(ticket_sudo, access_token, **kw)
        return request.render("helpdesk.tickets_followup", values)
