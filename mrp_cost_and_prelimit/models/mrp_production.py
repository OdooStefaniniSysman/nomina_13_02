# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # def button_mark_done(self):
    #     res = super(MrpProduction, self).button_mark_done()
    #     #self.create_move_test()
    #     return res

    def create_move_workcenter(self):
        am_obj = self.env['account.move']
        for record in self:
            product_id = record.product_id
            journal_id = product_id.categ_id.property_stock_journal
            if not journal_id:
                raise ValidationError("EL producto [%s] %s no tiene un diario asignado en su categoria" % (product_id.default_code, product_id.name))
            if record.routing_id:
                acc_move_ids = []
                for operation in record.routing_id.operation_ids:
                    line_ids = operation.workcenter_id._prepare_move_line(record.id, record.name)
                    if line_ids:
                        move = {
                            'journal_id': journal_id.id,
                            'line_ids': line_ids,
                            'date': fields.Date.today(),
                            'ref': record.name + ' - ' + operation.name,
                            'type': 'entry'
                        }
                        account_move = am_obj.sudo().create(move)
                        account_move.post()
                        acc_move_ids.append(account_move.id)
                # if acc_move_ids:
                #     return {
                #         'type': 'ir.actions.act_window',
                #         'name': 'Asientos ' + record.name,
                #         # 'view_type': 'tree',
                #         'view_mode': 'tree,form',
                #         'res_model': 'account.move',
                #         # 'res_id': acc_move_ids,
                #         'domain': [('id','in',acc_move_ids)],
                #         'target': 'current'}
    
    def create_move_test(self):
        am_obj = self.env['account.move']
        for record in self:
            
            product_id = record.product_id
            journal_id = product_id.categ_id.property_stock_journal

            if not journal_id:
                raise ValidationError("EL producto [%s] %s no tiene un diario asignado en su categoria" % (product_id.default_code, product_id.name))
            
            if record.routing_id:
                mod = []
                cif = []
                maq = []
                for workorder in record.workorder_ids:
                    workorder.button_pending()
                    #time = sum([x.duration for x in workorder.time_ids])
                    time= workorder.duration
                    time_corte= time
                    time = (time - workorder.estimated_time) / 60
                    cost_mod = workorder.workcenter_id.costs_hour_mod_real
                    cost_cif = workorder.workcenter_id.costs_hour_cif_real
                    cost_maq = workorder.workcenter_id.costs_hour_maq_real
                    account_mod = workorder.workcenter_id.mod_account_id_real
                    account_mod_c = workorder.workcenter_id.account_mod_id_real
                    account_cif = workorder.workcenter_id.cif_account_id_real
                    account_cif_c = workorder.workcenter_id.account_cif_id_real
                    account_maq = workorder.workcenter_id.maq_account_id_real
                    account_maq_c = workorder.workcenter_id.account_maq_id_real

                    # cost_mod = workorder.workcenter_id.costs_hour_mod
                    # cost_cif = workorder.workcenter_id.costs_hour_cif
                    # cost_maq = workorder.workcenter_id.costs_hour_maq
                    # account_mod = workorder.workcenter_id.mod_account_id
                    # account_mod_c = workorder.workcenter_id.account_mod_id
                    # account_cif = workorder.workcenter_id.cif_account_id
                    # account_cif_c = workorder.workcenter_id.account_cif_id
                    # account_maq = workorder.workcenter_id.maq_account_id
                    # account_maq_c = workorder.workcenter_id.account_maq_id
                    #########################################################################
                    if cost_mod == 0:
                        raise ValidationError("El costo MOD por hora no esta definido en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if cost_cif == 0:
                        raise ValidationError("El costo CIF por hora no esta definido en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if cost_maq == 0:
                        raise ValidationError("El costo MAQ por hora no esta definido en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if not account_mod:
                        raise ValidationError("La cuenta MOD no está definida en el centro productivo  [%s]" % workorder.workcenter_id.name)
                    if not account_mod_c:
                        raise ValidationError("La cuenta MOD de contrapartida no está definida en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if not account_cif :
                        raise ValidationError("El cuenta CIF no está definida en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if not account_cif_c:
                        raise ValidationError("El cuenta CIF de contrapartida no está definida en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if not account_maq:
                        raise ValidationError("El cuenta MAQ  no está definida en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    if not account_maq_c:
                        raise ValidationError("El cuenta MAQ de contrapartida no está definida en el centro productivo: [%s]" % workorder.workcenter_id.name)
                    # credit = 0.00
                    partner_id = record.company_id.partner_id.id
                    if time > 0.0:
                        if cost_mod and account_mod and account_mod_c:
                            
                            line = {
                                'name': record.name + ' - ' + workorder.workcenter_id.name,
                                'partner_id': partner_id,
                                'debit': time * cost_mod,
                                'credit': 0.00,
                                'account_id': account_mod.id
                                    }
                            mod.append((0,0,line))
                            line = {
                                'name': record.name + ' - ' + 'Contrapartida -' + workorder.workcenter_id.name,
                                'partner_id': partner_id,
                                'debit': 0.00,
                                'credit': time * cost_mod,
                                'account_id': account_mod_c.id
                            }
                            mod.append((0,0,line))
                            # credit += self.costs_hour_mod
                        if cost_cif and account_cif and account_cif_c:
                            line = {
                                'name': record.name + ' - ' + workorder.workcenter_id.name,
                                'partner_id': partner_id,
                                'debit': time * cost_cif,
                                'credit': 0.00,
                                'account_id': account_cif.id
                            }
                            cif.append((0,0,line))
                            line = {
                                'name': record.name + ' - ' + 'Contrapartida CIF'+ workorder.workcenter_id.name,
                                'partner_id': partner_id,
                                'debit': 0.00,
                                'credit': time * cost_cif,
                                'account_id': account_cif_c.id
                            }
                            cif.append((0,0,line))
                            # credit += self.costs_hour_cif
                        if cost_maq and account_maq and account_maq_c:
                            line = {
                                'name': record.name + ' - ' + workorder.workcenter_id.name,
                                'partner_id': partner_id,
                                'debit': time * cost_maq,
                                'credit': 0.00,
                                'account_id': account_maq.id
                            }
                            maq.append((0,0,line))
                            line = {
                                'name': record.name + ' - ' + 'Contrapartida MAQ'+ workorder.workcenter_id.name,
                                'partner_id': partner_id,
                                'debit': 0.00,
                                'credit': time * cost_maq,
                                'account_id': account_maq_c.id
                            }
                            maq.append((0,0,line))
                    query = ''' update mrp_workorder set estimated_time = %s where id = %s'''
                    self._cr.execute(query,(time_corte, workorder.id))
                    #workorder.estimated_time = time_corte
                    workorder.button_start()
                acc_move_ids = []
                if mod:
                    move = {
                        'journal_id': journal_id.id,
                        'line_ids': mod,
                        'date': fields.Date.today(),
                        'ref': record.name + ' - MOD',
                        'type': 'entry'
                    }
                    account_move = am_obj.sudo().create(move)
                    account_move.post()
                    acc_move_ids.append(account_move.id)
                if cif:
                    move = {
                        'journal_id': journal_id.id,
                        'line_ids': cif,
                        'date': fields.Date.today(),
                        'ref': record.name + ' - CIF',
                        'type': 'entry'
                    }
                    account_move = am_obj.sudo().create(move)
                    account_move.post()
                    acc_move_ids.append(account_move.id)
                if maq:
                    move = {
                        'journal_id': journal_id.id,
                        'line_ids': maq,
                        'date': fields.Date.today(),
                        'ref': record.name + ' - MAQ',
                        'type': 'entry'
                    }
                    account_move = am_obj.sudo().create(move)
                    account_move.post()
                    acc_move_ids.append(account_move.id)
    
    def automated_assent_line(self):

        line_assents = self.search([])
        line_assents.create_move_test()


    
    # def post_inventory(self):

    #     res = super(MrpProduction, self).post_inventory()
    #     for record in self:
    #         record.create_move_test()
    #     return res
