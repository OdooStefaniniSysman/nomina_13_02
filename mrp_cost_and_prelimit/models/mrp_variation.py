import itertools
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpVariation(models.Model):

    _name = 'mrp.variation'
    
    name = fields.Char('Anlásis de Variación')
    
    state = fields.Selection([('draft', 'Borrador'), 
                              ('confirm', 'Confirmado'),
                              ('accounted', 'Contabilizado'),
                              ('cancel', 'Cancelado')],'Estado', default="draft")
    production_ids = fields.Many2many('mrp.production', string = 'Orden de produccion')
    start_time = fields.Datetime('Fecha de inicio', required=True)
    end_time = fields.Datetime('Fecha fin', required=True)
    line_ids = fields.One2many('mrp.variation.line', 'variation_id', 'Detalle de Variaciones')
    journal_id = fields.Many2one('account.journal', 'Diario')
    action = fields.Many2one('ir.cron', 'Accion Automática')
      
    def block_workorders(self):
        self.ensure_one()
        mrp_wkc_prod_obj = self.env['mrp.workcenter.productivity']
        loss_id = self.env['ir.model.data'].get_object('mrp_cost_and_prelimit', 'mrp_workcenter_productivity_loss_variation')
        domain = []
        if self.production_ids:
            domain.append(('production_id','in',self.production_ids.ids))
        workorders = self.env['mrp.workorder'].search(domain)
        for ot in workorders.filtered(lambda x: x.state == 'progress' and x.working_state in ('normal', 'done')):
            vals = {
                'loss_id': loss_id.id,
                'description': 'Bloqueo por Análisis de Variaciones',
                'workcenter_id': ot.workcenter_id.id,
                'company_id': ot.company_id.id
            }
            mrp_wkc_prod_id = mrp_wkc_prod_obj.create(vals)
            mrp_wkc_prod_id.button_block()

    
    def generate_report(self):
        self.ensure_one()
        self.line_ids.unlink()
        mrp_var_line_obj = self.env['mrp.variation.line']
        domain = []
        if self.production_ids:
            domain.append(('production_id','in',self.production_ids.ids))
            domain.append(('date_planned_start','>',self.start_time))
            domain.append(('date_planned_start','<',self.end_time))
            
    
        workorders = self.env['mrp.workorder'].search(domain)
        

        workorder_prog = [x.display_name for x in workorders.filtered(lambda x: x.state == 'progress' and x.working_state in ('normal', 'done'))]
        if workorder_prog:
            raise ValidationError('Las siguientes Ordenes de Trabajo estan en proceso. \n' 
                                    'Por favor bloquearlas para generar el reporte. \n\n'
                                    '%s' % workorder_prog)

        
        var_lines_ids = []
        for workorder in workorders:
            time = sum([x.duration for x in workorder.time_ids])/60
            time_estimated = (workorder.duration_expected)/60
            time_real_operator = sum([x.real_time_operator_line for x in workorder.time_ids])/60

            # plannifiqued = self.production_ids.product_qty
            plannifiqued = workorder.qty_production
            
            if not self.production_ids.finished_move_line_ids:
                raise ValidationError('Deben haber productos finalizados en la orden seleccionada')
            else:
                produced=workorder.production_id.qty_produced

            # Costos Estandar
            mod_standard = time_estimated * workorder.workcenter_id.costs_hour_mod
            cif_standard = time_estimated * workorder.workcenter_id.costs_hour_cif
            maq_standard = time_estimated * workorder.workcenter_id.costs_hour_maq 
            # Costos Reales
            mod_real = time_real_operator * workorder.workcenter_id.costs_hour_mod_real
            cif_real = time * workorder.workcenter_id.costs_hour_cif_real
            maq_real = time * workorder.workcenter_id.costs_hour_maq_real
            # Costos de Variacion
            mod_variation = ((mod_standard - mod_real)/plannifiqued)*produced
            cif_variation = ((cif_standard - cif_real)/plannifiqued)*produced
            maq_variation = ((maq_standard - maq_real)/plannifiqued)*produced

            # mod_variation = mod_standard - mod_real
            # cif_variation = cif_standard - cif_real
            # maq_variation = maq_standard - maq_real

           
            vals = {
                'variation_id': self.id,
                'workorder_id': workorder.id,
                'production_id': workorder.production_id.id or False,
                'product_id': workorder.product_id.id or False,
                'qty_planned': workorder.qty_production,
                'qty_finished': workorder.qty_produced,
                'state': workorder.state,
                'cif_standard': cif_standard,
                'maq_standard': maq_standard,
                'mod_standard': mod_standard,
                'mod_real': mod_real,
                'cif_real': cif_real,
                'maq_real': maq_real,
                'mod_variation': mod_variation,
                'cif_variation': cif_variation,
                'maq_variation': maq_variation,
            }
            var_line = mrp_var_line_obj.create(vals)
            var_lines_ids.append(var_line.id)

        #  if  len(workorders)>0:
        #      cantidad_esperada = workorder.qty_production   
        #      cantidad_total = [y.qty_finished for y in self.line_ids][-1]
        #      total_real = sum([y.mod_real for y in self.line_ids]) + sum([y.cif_real for y in self.line_ids]) + sum([y.maq_real for y in self.line_ids])  
        #      total_standard = sum([y.mod_standard for y in self.line_ids]) + sum([y.cif_standard for y in self.line_ids]) + sum([y.maq_standard for y in self.line_ids])  
        #      total_variation = sum([y.mod_variation for y in self.line_ids]) + sum([y.cif_variation for y in self.line_ids]) + sum([y.maq_variation for y in self.line_ids])        
            
        #      self.production_ids.total_variation_real = (total_real/cantidad_esperada)*cantidad_total
        #      self.production_ids.total_variation_standard = (total_standard/cantidad_esperada)*cantidad_total
        #      self.production_ids.total_variation_variation = total_variation

        return {
            'type': 'ir.actions.act_window',
            'name': 'Anlálisis de Variaciones',
            # 'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'mrp.variation.line',
            # 'res_id': acc_move_ids,
            'domain': [('id','in',var_lines_ids)],
            'target': 'current'
        }

    def go_to_variation_lines(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Anlálisis de Variaciones',
            # 'view_type': 'tree',
            'view_mode': 'tree',
            'res_model': 'mrp.variation.line',
            # 'res_id': acc_move_ids,
            'domain': [('id','in',self.line_ids.ids)],
            'target': 'current'
        }

    def state_to_confirm(self):
        self.ensure_one()
        self.state = 'confirm'

    def state_to_cancel(self):
        self.ensure_one()
        if self.state == 'accounted':
            raise ValidationError('No se puede cancelar un documento de Análisis de Variaciones Contabilizado')
        
        self.state = 'cancel'
    
    def state_to_accounted(self):
        self.ensure_one()
        self.state = 'accounted'

    def generate_account_moves(self):
        self.ensure_one()
        am_obj = self.env['account.move']

        if not self.journal_id:
            raise ValidationError('No existe un diario')

        for key,line in itertools.groupby(self.line_ids,lambda x: x.production_id):
            lines = []
            for y in line:
                partner_id = y.workorder_id.company_id.partner_id.id
                sum_variation = 0
                sum_variation = y.mod_variation + y.cif_variation + y.maq_variation
                account_variation = y.workorder_id.workcenter_id.account_variation
                account_variation_c = y.workorder_id.workcenter_id.account_close_variation
                if not account_variation or not account_variation_c:
                    raise ValidationError('Las cuentas de variación no están definidias en el centro productivo: %s'
                     %y.workorder_id.workcenter_id.name )

                line = {
                    'name': key.name + ' - ' + y.workorder_id.workcenter_id.name,
                    'partner_id': partner_id,
                    'debit': abs(sum_variation) if sum_variation > 0 else 0.0,
                    'credit': 0.00 if sum_variation > 0 else abs(sum_variation),
                    'account_id': account_variation.id
                        }
                lines.append((0,0,line))
                
                line = {
                    'name': key.name + ' - ' + 'Contrapartida -' + y.workorder_id.workcenter_id.name,
                    'partner_id': partner_id,
                    'debit': 0.00 if sum_variation > 0 else abs(sum_variation),
                    'credit': abs(sum_variation) if sum_variation > 0 else 0.0,
                    'account_id': account_variation_c.id
                    }
                lines.append((0,0,line))


            move = {
                'journal_id': self.journal_id.id,
                'line_ids': lines,
                'date': fields.Date.today(),
                'ref': key.name + ' - Variación',
                'type': 'entry'
                    }
            account_move = am_obj.sudo().create(move)
            account_move.post()
        
        self.state_to_accounted()
        

    


    


