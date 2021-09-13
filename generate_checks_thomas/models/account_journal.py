# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountJournaThomas(models.Model):
    _inherit = 'account.journal'
    _description = "Diarios"
     
    sequence_until = fields.Char(string="Del")
    sequence_since = fields.Char(string="Hasta")
    alpha_code = fields.Char()
    concatenation = fields.Char(string="Concatenación", compute='_get_check_next_number_thomas', inverse='_set_check_next_number_thomas')
    check_sequence_id_thomas = fields.Many2one('ir.sequence', 'Cod. Alfabético',copy=False,help="Checks numbering sequence.")
    sequence_concatenation = fields.Char(string="Secuencia")
    prefix = fields.Char(string="Prefijo", related="check_sequence_id_thomas.prefix")

    @api.onchange('prefix','concatenation')                  
    def _onchange_concatenation_Seq(self):
        self.sequence_concatenation = "%s %s" % (
            self.check_sequence_id_thomas.name if self.check_sequence_id_thomas.name else "",          
            self.concatenation if self.concatenation else "")

    @api.depends('check_manual_sequencing')
    def _get_check_next_number_thomas(self):
        for journal in self:
            if journal.check_sequence_id_thomas:
                journal.concatenation = journal.check_sequence_id_thomas.number_next_actual
            else:
                journal.concatenation = 1

    def _set_check_next_number_thomas(self):
        for journal in self:
            if journal.concatenation and not re.match(r'^[0-9]+$', journal.concatenation):
                raise ValidationError(_('Este Campo  solo debe contener numeros.'))
            if int(journal.concatenation) < journal.check_sequence_id_thomas.number_next_actual:
                raise ValidationError(_("El último numero registado en un cheque fue %s. Con el fin de evitar un rechazo con el banco,"
                    "sólo se puede utilizar un número mayor al anterior.") % journal.check_sequence_id_thomas.number_next_actual)
            if journal.check_sequence_id_thomas:
                journal.check_sequence_id_thomas.sudo().number_next_actual = int(journal.concatenation)

    @api.model
    def create(self, vals):
        rec = super(AccountJournaThomas, self).create(vals)
        if not rec.check_sequence_id_thomas:
            rec._create_check_sequence_thomas()
        return rec

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        rec = super(AccountJournaThomas, self).copy(default)
        rec._create_check_sequence_thomas()
        return rec            

    def _create_check_sequence_thomas(self):
        """ Create a check sequence for the journal """
        for journal in self:
            journal.check_sequence_id_thomas = self.env['ir.sequence'].sudo().create({
                'name': journal.name + _(" : Check Number Sequence"),
                'implementation': 'no_gap',
                'padding': 8,
                'number_increment': 1,
                'company_id': journal.company_id.id,
            })

    #@api.constrains('sequence_until')
    #def _check_validate_since_and_until(self):
        #for record in self:
        	#if record.type == 'bank':
	            #if record.int(concatenation) > record.int(sequence_until):
	                #raise ValidationError("El valor Final de la secuencia no puede ser menor al valor inicial  : %s" % record.sequence_until)                                    

   


   
   







    
    
    
