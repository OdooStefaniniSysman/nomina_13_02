from odoo import models, fields, api

class HelpdeskHelpdesk(models.Model):
    _name = 'helpdesk.helpdesk'

    name = fields.Char(string='Name helpdesk')
    team_id = fields.Many2one('helpdesk.team', string='Team Helpdesk')
    helpdesk_team_tipology = fields.Char(compute='_get_label_team', string='Helpdesk Tipology', store=True)
    helpdesk_ticket_ids = fields.One2many('helpdesk.ticket', 'helpdesk_id', string='Ticket Helpdesk', )
    
    @api.depends('team_id')
    def _get_label_team(self):
        for record in self:
            if record.team_id.name == 'MESA DE AYUDA SEGURIDAD':
                record.helpdesk_team_tipology = 'SEGURIDAD'
            elif record.team_id.name == 'MESA DE AYUDA TECNOLOGÍA':
                record.helpdesk_team_tipology = 'TECNOLOGÍA'
            else:
                record.helpdesk_team_tipology = False

    def filter_helpdesk_name(self):       
        return {
            'type': 'ir.actions.act_window',
            'name': self.helpdesk_team_tipology,
            # 'view_type': 'tree',
            'view_mode': 'kanban,form,tree',
            'res_model':  'helpdesk.ticket',
            #'team_id': self.team_id.id,
            # 'res_id': acc_move_ids,
            'domain': [('team_id','=',self.team_id.id),('create_uid','=',self.env.user.user_ids.id)],
            'context': {'default_team_id': self.team_id.id},
            'target': 'current'
        }



