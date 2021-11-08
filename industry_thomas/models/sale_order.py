#Luis Felipe Paternina
#Ingeniero de Sistemas
#Todoo SAS
from odoo import models, fields, api

class Todoo(models.Model):
    _inherit = 'sale.order'

    order_class = fields.Char(string="Clase de Pedido", default="ZP01")
    org_vtg = fields.Char(string="Org Vtas", default="1100")    
    channel = fields.Char(string="Canal", default="10")  
    sector = fields.Char(string="Sector", default="12")
    cebe = fields.Char(string="Cebe", default="1140010124")
    currency_tst = fields.Char(string="Moneda", default="CP1")
    sequence_maintenance = fields.Char(string="# de Petición")
    sap_code = fields.Char(related="partner_id.sap", string="Código SAP")
    time_of = fields.Char(string="Tiempo de Entrega")
    date_of_attention = fields.Datetime(string="Fecha de Atención")
    type_of_servicetst = fields.Selection([('correctivo','Correctivo'),('preventivo','Preventivo'),('instalacion de maquina','Instalación de Maquina'),('alistamiento','Alistamiento'),('instalacion de repuesto','Instalación de Repuesto'),('garantia','Garantía')], string="Tipo de Servicio")
    technical_tst =  fields.Many2one('res.users',string="Técnico")
    technical_code = fields.Char(related="technical_tst.technical_code", string="Código del Técnico")
    branch_tst = fields.Many2one('res.city', string="Sucursal")
    office_code = fields.Char(string="Código de Oficina - Sucursal")
    address_branch_tst = fields.Char(string="Dirección de Sucursal")
    description_maintenance = fields.Text(string="Descripción del Mantenimiento")
    stage_maintenance = fields.Char(string="Estado del Servicio")
    check_tag_ids = fields.Boolean(compute='_compute_check_tag_ids')
    stageid = fields.Char(string="Estado del Servicio", default="FINALIZADO")
    type_of_guarantee_sale = fields.Selection([('venta','Garantía por Venta'),('mantenimiento','Garantía por Mantenimiento')], string="Tipo de Garantía",tracking=True)
    charge_service = fields.Selection([('si','Si'),('no','No')], string="Se cobra Servicio?",default='si')
    charge_spare = fields.Selection([('si','Si'),('no','No')], string="Se cobra Repuesto?", default='si')
    charge_service_gar = fields.Selection([('si','Si'),('no','No')], string="Se cobra Servicio?",default='no')
    charge_spare_gar = fields.Selection([('si','Si'),('no','No')], string="Se cobra Repuesto?", default='si')
    charge_service_garv = fields.Selection([('si','Si'),('no','No')], string="Se cobra Servicio?",default='no')
    charge_spare_garv = fields.Selection([('si','Si'),('no','No')], string="Se cobra Repuesto?", default='no')
    service_total = fields.Float(string="Total del Servicio")
    spare_total = fields.Float(string="Total del Repuesto")
    serial = fields.Char(string="Serial")
    brand = fields.Char(string="Marca")
    model_tst = fields.Char(string="Modelo")
    machine_tsts = fields.Many2one('maintenance.equipment', string="Máquina")
    city_of_machine = fields.Many2one('res.city', related="machine_tsts.branch", string="Ciudad")
    branch_machine = fields.Char(related="machine_tsts.branch_tst")
    state_machine = fields.Many2one('res.country.state', related="machine_tsts.department")
    machine_catg = fields.Many2one('maintenance.equipment.category', related="machine_tsts.category_id", string="Categoría del Equipo")
    service_total = fields.Monetary(string="Total del Servicio", compute="_amount_service_total", currency_id="company_id.currency_id", store=True, readonly=True,)
    spare_total = fields.Monetary(string="Total del Repuesto", compute="_amount_product_total", currency_id="company_id.currency_id", store=True, readonly=True,)
    create_on_datetime=fields.Datetime('Fecha de Creación',tracking=True, default= fields.Datetime().now())
    

    @api.depends('state')
    def _compute_check_tag_ids(self):
        for record in self:
            record.check_tag_ids = True if record.state  == 'sale' else False

    
    @api.depends('order_line.price_total')
    def _amount_service_total(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                if line.product_id.type == 'service':
                    amount_untaxed += line.price_subtotal
                    amount_tax += line.price_tax
            order.update({
                'service_total': amount_untaxed + amount_tax,
            })
            
            
    @api.depends('order_line.price_total')
    def _amount_product_total(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                if line.product_id.type == 'product':
                    amount_untaxed += line.price_subtotal
                    amount_tax += line.price_tax
            order.update({
                'spare_total': amount_untaxed + amount_tax,
            })

    