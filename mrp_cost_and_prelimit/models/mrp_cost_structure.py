# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpCostStructure(models.AbstractModel):
    _inherit = 'report.mrp_account_enterprise.mrp_cost_structure'

    def get_lines(self, productions):
        res = super(MrpCostStructure, self).get_lines(productions)
        ProductProduct = self.env['product.product']
        count = 0
        for product in productions.mapped('product_id'):
            mos = productions.filtered(lambda m: m.product_id == product)
            #get the cost of operations line
            operations_line = []
            Workorders = self.env['mrp.workorder'].search([('production_id', 'in', mos.ids)])
            if Workorders:
                query_str = """SELECT w.operation_id, op.name, partner.name, sum(t.duration), wc.costs_hour, wc.costs_hour_mod, wc.costs_hour_cif, wc.costs_hour_maq
                                FROM mrp_workcenter_productivity t
                                LEFT JOIN mrp_workorder w ON (w.id = t.workorder_id)
                                LEFT JOIN mrp_workcenter wc ON (wc.id = t.workcenter_id )
                                LEFT JOIN res_users u ON (t.user_id = u.id)
                                LEFT JOIN res_partner partner ON (u.partner_id = partner.id)
                                LEFT JOIN mrp_routing_workcenter op ON (w.operation_id = op.id)
                                WHERE t.workorder_id IS NOT NULL AND t.workorder_id IN %s
                                GROUP BY w.operation_id, op.name, partner.name, t.user_id, wc.costs_hour, wc.costs_hour_mod, wc.costs_hour_cif, wc.costs_hour_maq
                                ORDER BY op.name, partner.name
                            """
                self.env.cr.execute(query_str, (tuple(Workorders.ids), ))
                for op_id, op_name, user, duration, cost_hour, cost_hour_mod, costs_hour_cif, costs_hour_maq in self.env.cr.fetchall():
                    operations_line.append([user, op_id, op_name, duration / 60.0, cost_hour, cost_hour_mod, costs_hour_cif, costs_hour_maq])
            res[count]['operations_line'] = operations_line
            #get the cost of raw material effectively used
            raw_material_moves_line = []
            query_str = """SELECT sm.product_id, sm.bom_line_id, abs(SUM(sml.qty_done)), abs(SUM(sm.price_unit))
                             FROM stock_move AS sm
                             INNER JOIN stock_move_line AS sml ON sml.move_id = sm.id
                            WHERE sm.raw_material_production_id in %s AND sm.state != 'cancel' AND sm.product_qty != 0 AND scrapped != 't'
                         GROUP BY sm.bom_line_id, sm.product_id"""
            self.env.cr.execute(query_str, (tuple(mos.ids), ))
            for product_id, bom_line_id, qty, cost in self.env.cr.fetchall():
                raw_material_moves_line.append({
                    'qty': qty,
                    'cost': cost,
                    'product_id': ProductProduct.browse(product_id),
                    'bom_line_id': bom_line_id
                })
            res[count]['raw_material_moves_line'] = raw_material_moves_line
            # Costs before
            cost_planned = []
            query_str = """select pp.id as product_id,
                        '' as product,
                        round((mp.product_qty * mbl.product_qty)/mb.product_qty,2) as quantity,
                        ip.value_float as cost,
                        round(((mp.product_qty * mbl.product_qty)/mb.product_qty)*cast(ip.value_float as numeric),2) as total 
                        from mrp_bom_line mbl 
                        inner join product_product pp on pp.id = mbl.product_id 
                        inner join ir_property ip on  ip.res_id = 'product.product,' || cast(pp.id as character varying) and ip.name = 'standard_price'
                        inner join mrp_bom mb on mb.id = mbl.bom_id 
                        inner join mrp_production mp on mp.bom_id = mb.id 
                        where mp.id in %s"""
            self.env.cr.execute(query_str, (tuple(mos.ids), ))
            for product_id, product, quantity, cost, total in self.env.cr.fetchall():
                cost_planned.append({
                    'product_id': ProductProduct.browse(product_id),
                    'product': product,
                    'quantity': quantity,
                    'cost': cost,
                    'total': total
                })
            query_str = """select '' as product_id,
                        wc.name as product,
                        cast(mrw.time_cycle_manual/60 as numeric) as quantity,
                        wc.costs_hour as cost,
                        (mrw.time_cycle_manual/60) * wc.costs_hour as total 
                        from mrp_routing_workcenter mrw 
                        inner join mrp_workcenter wc on wc.id = mrw.workcenter_id 
                        inner join mrp_routing mr on mr.id = mrw.routing_id 
                        inner join mrp_production mp on mp.routing_id = mr.id 
                        where mp.id in %s"""
            self.env.cr.execute(query_str, (tuple(mos.ids), ))
            for product_id, product, quantity, cost, total in self.env.cr.fetchall():
                cost_planned.append({
                    'product_id': product_id,
                    'product': product,
                    'quantity': quantity,
                    'cost': cost,
                    'total': total
                })
            res[count]['cost_planned'] = cost_planned
            count += 1
        return res