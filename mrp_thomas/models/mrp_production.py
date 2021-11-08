#Luis Felipe Paternina
#Todoo SAS
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class MprProduction(models.Model):
    _inherit = 'mrp.production'

    date_of_elaboration = fields.Datetime(string="Fecha Elaboración", tracking=True, default= fields.Datetime().now())
    about_technical = fields.Integer(string="Sobre Técnico")
    sale_order_id = fields.Many2one('sale.order', string="Pedido de Venta")
    partner_client_id = fields.Many2one(related="sale_order_id.partner_id", string="Cliente")
    art_elaboration = fields.Selection(related="sale_order_id.elaboration_art_type")
    order_reference = fields.Char(related="sale_order_id.prev_order", string="Referencia Orden Anterior")
    design = fields.Selection(related="sale_order_id.design_type")
    delivery_date_th = fields.Datetime(related="sale_order_id.commitment_date", string="Fecha de Entrega")
    order_type = fields.Selection([('semi','Semielaborado'),('per','Personalización'),('muestra','Muestra'),('reimpresion','Reimpresión')], string="Tipo de Orden")
    print_set = fields.Char(string="SET de Impresión")
    printing_line = fields.Selection(related="sale_order_id.printing_line_type")
    ctp = fields.Text(string="CTP")
    design_and_assembly = fields.Text(string="Diseño y Montaje")
    stroke_art = fields.Text(string="Trazo, Arte o Muestra Aprobado")
    kind_of_paper = fields.Many2one(related="sale_order_id.mrp_kind_of_paper_id")
    visible_background = fields.Text(string="Fondo Visible")
    invisible_background = fields.Text(string="Fondo Invisible")
    logo = fields.Text(string="Logotipo")
    text = fields.Text(string="Textos")
    microtext = fields.Text(string="Microtextos")
    texts = fields.Text(string="Textos")
    fringe = fields.Text(string="Orla")
    microtexts = fields.Text(string="Microtextos")
    imprint = fields.Text(string="Pie de Imprenta")
    latent_image = fields.Text(string="Imagen Latente")
    etc = fields.Text(string="Etc.")
    leaf_waste = fields.Integer(string="Desperdicio en Hojas")
    waste_percentage = fields.Integer(related="leaf_waste" ,string="Desperdicio en Porcentaje")
    number_of_sheets = fields.Text(string="Cantidad de Hojas")
    amount_of_kilos = fields.Text(string="Cantidad de Kilos")
    description_of_role = fields.Text(string="Descripción del Papel")
    sheet_size = fields.Text(string="Tamaño Hoja")
    cut_size = fields.Text(string="Tamaño de Corte")
    number_sheets = fields.Text(string="Cantidad de Hojas")
    waste = fields.Text(string="Desperdicio de Hojas")
    waste_percentage1 = fields.Text(string="Desperdicio en Porcentaje")
    printing_set_1 = fields.Text(string="SET de Impresión")
    since_numeration = fields.Char(string="Numeración Desde", related="sale_order_id.since")
    until_numeration = fields.Char(string="Numeración Hasta", related="sale_order_id.until")
    digits_numbers = fields.Char(string="No.Digitos", related="sale_order_id.number_of_digits")
    position = fields.Char(string="Posición", related="sale_order_id.position")
    prefix = fields.Selection(related="sale_order_id.prefix_type", string="Prefijo")
    half_cut = fields.Selection(related="sale_order_id.half_cut_type", string="Medio Corte")
    security_die = fields.Selection(related="sale_order_id.security_die_type", string="Troquel de Seguridad")
    printt = fields.Selection(related="sale_order_id.stamping_type", string="Estampado")
    ribbon_color = fields.Char(related="sale_order_id.ribbon_color", string="Color Cinta Estampado")
    design_print = fields.Char(related="sale_order_id.design_to_print", string="Diseño a Estampar")
    perforated_type = fields.Selection(related="sale_order_id.perforated_type", string="Perforado")
    personalitation_sale = fields.Selection(related="sale_order_id.personalization", string="Personalización")
    location_sale = fields.Char(related="sale_order_id.customization_location", string="Ubicación de la Personalización")
    type_of_information = fields.Char(related="sale_order_id.type_of_information", string="Tipo de Información")
    type_of_personalization = fields.Char(related="sale_order_id.type_of_customization", string="Tipo de Personalización")
    numbers_sale = fields.Char(related="sale_order_id.customization_numbering", string="Numeración")
    quantity_package = fields.Char(related="sale_order_id.quantity_package", string="Cantidad por Empaque")
    custody = fields.Selection(related="sale_order_id.custody", string="Custodia")
    packaging_label = fields.Char(related="sale_order_id.packaging_label", string="Especificación del Rotulo de Empaque")
    type_of_box = fields.Char(string="Tipo de Caja")
    material_specifications = fields.Text(string="Especificación de Materiales Adicionales")
    sample_quantities = fields.Char(string="Cantidad de Muestras Númeradas en Ceros")
    customer_to_bill = fields.Char(related="sale_order_id.customer_to_bill", string="Cliente")
    billable = fields.Selection(related="sale_order_id.billable", string="Facturable")
    number_of_leaves = fields.Char(string="Cantidad de Hojas")
    leaf_waste_sale = fields.Char(string="Desperdicio de Hojas")
    waste_percentage_sale = fields.Char(string="Porcentaje de Desperdicio")
    set_impresion1_sale = fields.Char(string="SET de Impresión")
    ctp_sale = fields.Text(string="CTP")
    logo_qweb = fields.Binary(related="company_id.logo", string="Logo")
    workcenter_line_ids = fields.One2many('mrp.production.routing.workcenter','routing_production_id', 'Centro de Producción')
    res_city_id = fields.Many2one(related="sale_order_id.res_city_id")
    type_of_client = fields.Selection(related="sale_order_id.sale_type")
    date_order_sale = fields.Datetime(related="sale_order_id.date_order")
    user_id_sale = fields.Many2one(related="sale_order_id.user_id")
    number_of_quotation = fields.Char(string="Numero de Cotización")
    date_of_quotation = fields.Datetime(string="Fecha de Cotización", related="sale_order_id.date_order")
    option = fields.Char(string="Opción")
    width = fields.Char(related="sale_order_id.width", string="Ancho")
    heigth = fields.Char(related="sale_order_id.heigth", string="Largo")
    grammage = fields.Char(related="sale_order_id.grammage", string="Gramaje")
    since = fields.Char(related="sale_order_id.since", string="Desde")
    until = fields.Char(related="sale_order_id.until", string="Al")
    is_test = fields.Boolean(related="sale_order_id.is_a_test", string="Es una Prueba")
    test_name = fields.Char(related="sale_order_id.test_name", string="Nombre de la Prueba")
    date_of_application = fields.Date(related="sale_order_id.date_of_application", string="Fecha de Aplica")
    is_lottery = fields.Boolean(related="sale_order_id.is_lottery", string="Es una Loteria")
    draw = fields.Char(related="sale_order_id.draw", string="Sorteo")
    fractions_bills = fields.Integer(related="sale_order_id.fractions_bills", string="Fracciones de Billetes")
    game_date = fields.Date(related="sale_order_id.game_date", string="Fecha de Juego")
    width_fraction_size = fields.Char(string="Ancho", related="sale_order_id.width_fraction_size")
    heigth_fraction_size = fields.Char(string="Largo", related="sale_order_id.heigth_fraction_size")
    number_tickets = fields.Integer(string="Cantidad de Tickets por Rollos", related="sale_order_id.number_tickets")
    number_of_rolls = fields.Integer(string="Numeración de Cajas", related="sale_order_id.number_of_rolls")
    wide_head_size = fields.Char(string="Ancho", related="sale_order_id.wide_head_size")
    heigth_head_size = fields.Char(string="Largo", related="sale_order_id.heigth_head_size")
    rolls_since = fields.Char(string="Desde", related="sale_order_id.rolls_since")
    rolls_until = fields.Char(string="Al", related="sale_order_id.rolls_until")
    numeration = fields.Boolean(string="Numeración", related="sale_order_id.numeration")
    general_description = fields.Text(string="Preliminares")
    description_th = fields.Text(string="Observaciones")
    area = fields.Selection([('planas','Formas Planas'),('continuas','Formas Continuas'),('personalizacion','Personalización')], string="Area")
    date_deadline = fields.Date(string="Fecha límite", related="sale_order_id.validity_date")
    check_thomas_colombia = fields.Boolean(string="Validar Desarrollos Thomas Colombia", compute="_compute_check_company_id")
   
    
    @api.depends('company_id')
    def _compute_check_company_id(self):
        for record in self:
            record.check_thomas_colombia = True if record.company_id and record.company_id[0].name  == 'THOMAS GREG & SONS DE COLOMBIA S.A.' else False

    @api.onchange('routing_id')
    def _onchange_mrp_routing_thomasprod(self):
        for rec in self:
                lines = []
                rec.workcenter_line_ids = lines
                
                for line in self.workcenter_line_ids:
                    rec.write({'workcenter_line_ids': [( 2, line.id)]})
                for line in self.routing_id.operation_ids:
                    _logger.error("+*************************************************************")
                    _logger.error(line)
                    _logger.error(line.time_cycle)
                    vals = {
                        'name': line.name,
                        'workcenter_id': line.workcenter_id.id,
                        'time_cycle': line.time_cycle,
                        'routing_production_id': line.id,
                        'routing_id': line.routing_id.id,
                    }
                    lines.append((0,0,vals))
                rec.workcenter_line_ids = lines   
                    

                
              


         

 
    