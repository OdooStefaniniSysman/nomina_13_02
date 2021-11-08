# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, tools, api,_
from datetime import datetime
from odoo.osv import expression
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)

    
class ZppReportLine(models.Model):
    _name = 'report.zpp'
    _auto = False
    _description = 'This is the lines in the zpp report'
    
    name = fields.Char('Production Order',readonly=True)
    date_planned_start = fields.Datetime('Start Date',readonly=True)
    date_planned_finished = fields.Datetime('End Date',readonly=True)
    product_id = fields.Many2one('product.product','Product',readonly=True)
    product_qty = fields.Float('Quantity Planned',readonly=True)
    description = fields.Char('Description',readonly=True)
    sale = fields.Char('No.Order',readonly=True)
    amount_total = fields.Float('Sale Price',readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account','Description Account Analytic',readonly=True)
    product_delivery = fields.Float('Delivered quantity',readonly=True)
    product_requisition = fields.Char('Third Service',readonly=True)
    code = fields.Char('Account Analytic',readonly=True)
    mod_real = fields.Float('Workforce Cost',readonly=True)
    cif_real = fields.Float('CIF Cost',readonly=True)
    maq_real = fields.Float('Machine Cost',readonly=True)
    currency_id = fields.Many2one('res.currency','Currency',readonly=True)
    standard_price = fields.Float('Cost x Unit',readonly=True)
    value = fields.Float('Material cost')
    total_cost = fields.Float('Total Cost')
    liquidation_order = fields.Float('Liquidation Order')
    entry = fields.Float('Entry')
    
    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_zpp')
        query = """
        CREATE or REPLACE VIEW report_zpp AS(
        
        select 
        row_number() OVER (ORDER BY mp.id) as id,
        mp.name,mp.date_planned_start,
        mp.date_planned_finished,
        mp.product_id,mp.product_qty as product_qty,
        mp.product_qty as product_delivery,
        so.name as sale,so.amount_total,so.analytic_account_id,
        --so.currency_id,
        aaa.code,
        --mprl.product_id as product_requisition,
        --mvl.mod_real,mvl.cif_real,mvl.maq_real,
        ( 
            select sum(mod_real)
            from mrp_variation_line mvl
            where mvl.production_id = mp.id
        
        ) as mod_real,
        ( 
            select sum(cif_real)
            from mrp_variation_line mvl
            where mvl.production_id = mp.id
        
        ) as cif_real,
        ( 
            select sum(maq_real)
            from mrp_variation_line mvl
            where mvl.production_id = mp.id
        
        ) as maq_real,
        (
            select sol.name
            from sale_order_line sol
            left join sale_order so on so.id = sol.order_id 
            where so.manufacture_id = mp.id
            and sol.product_id = mp.product_id
        ) as description,
        (
            select sol.standard_price
            from sale_order_line sol
            left join sale_order so on so.id = sol.order_id 
            where so.manufacture_id = mp.id
            and sol.product_id = mp.product_id
        ) as standard_price,
        (
            select sol.currency_id
            from sale_order_line sol
            left join sale_order so on so.id = sol.order_id 
            where so.manufacture_id = mp.id
            and sol.product_id = mp.product_id
            limit 1
        ) as currency_id,
        (
            select
            abs(SUM(svl.value)) FROM stock_move AS sm full join      
            stock_valuation_layer AS svl ON svl.stock_move_id = sm.id 
            where mp.id = sm.raw_material_production_id
        )  as value,
        ( 
            select sum(svl.value)
            from mrp_production mp2
            left join material_purchase_requisition mpr on mp.id = mpr.production_id
            left join material_purchase_requisition_line mprl on mprl.requisition_id = mpr.id
            left join product_product pp on mprl.product_id = pp.id
            left join stock_valuation_layer svl on svl.product_id = pp.id
            where mp2.id = mp.id

        ) as product_requisition,
        
        (
            select sum(value)
            from (
                select
                abs(SUM(svl.value)) as value
                FROM stock_move AS sm full join      
                stock_valuation_layer AS svl ON svl.stock_move_id = sm.id 
                where mp.id = sm.raw_material_production_id

                UNION ALL
                
                select sum(mvl.mod_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                
                UNION ALL
                
                select sum(mvl.cif_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                
                UNION ALL
                
                select sum(mvl.maq_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id

            ) as sum_total
        ) as total_cost,
        (
            select sum(value)
            from(
                select sum(mvl.mod_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                
                UNION ALL
                
                select sum(mvl.cif_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                
                UNION ALL
                
                select sum(mvl.maq_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                ) as liquidation_order

        ) as liquidation_order,
        (
            
            select sum(value)
            from (
                select sol.price_subtotal * -1 as value
                from sale_order_line sol
                left join sale_order so on so.id = sol.order_id 
                where so.manufacture_id = mp.id
                and sol.product_id = mp.product_id
                
                UNION ALL
                
                select
                abs(SUM(svl.value)) as value
                FROM stock_move AS sm full join      
                stock_valuation_layer AS svl ON svl.stock_move_id = sm.id 
                where mp.id = sm.raw_material_production_id

                UNION ALL
                
                select sum(mvl.mod_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                
                UNION ALL
                
                select sum(mvl.cif_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id
                
                UNION ALL
                
                select sum(mvl.maq_real) as value
                from mrp_variation_line mvl
                where mvl.production_id = mp.id

            ) as sum_total
        )as entry
        from mrp_production mp 
        --left join mrp_variation_line mvl on (mvl.production_id = mp.id)
        left join sale_order so on (so.manufacture_id = mp.id)
        --left join sale_order_line sol on(sol.order_id = so.id)
        left join account_analytic_account aaa on(aaa.id = so.analytic_account_id)
        --left join material_purchase_requisition mpr on (mpr.production_id = mp.id)
        --left join material_purchase_requisition_line mprl on (mprl.requisition_id = mpr.id)
        
        where 1=1
        );
        """
        self.env.cr.execute(query)
        #(select to_char(mp.date_planned_start,'mm')) as month,