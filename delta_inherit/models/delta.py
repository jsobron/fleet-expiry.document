from odoo import models, fields, api

class FleetMapSheet(models.Model):
    _inherit = 'fleet.map.sheet' 

    origin = fields.Char(string="Origen", required=True)  # Campo de origen, obligatorio
    destination = fields.Char(string="Destino", required=True)  # Campo de destino, obligatorio
    client = fields.Char(string="Cliente", required=True)  
    kg = fields.Float(string="Kilogramos", required=True)
    one_eight = fields.Float(string='Total 0.18', readonly=True, compute= "_compute_one_eight")
    total_gan = fields.Float(string='Ganancia total', readonly= True, compute= "_compute_gan")
    #Redifinicion de campos
    date = fields.Date(string='Fecha', readonly=False)
    distance_total = fields.Float(string='Distancia total', readonly=False)
    amount_total = fields.Float(string='Total', readonly=False)
    driver2_id = fields.Many2one('res.partner', string='Driver 2', required=False)
    #Used
    used_peaje = fields.Boolean(string='Peaje')
    varios = fields.Boolean(string='Varios')
    used_stay = fields.Boolean(string="Estadia")
    advances = fields.Boolean(string='Adelantos')

    #Total
    peaje_total = fields.Float(string='Total Gastado en Peaje')
    varios_total = fields.Float(string='Gastado en Varios')
    stay_total = fields.Float(string='Gasto en estadia')
    advances_total = fields.Float(string='$ Adelantos')



    @api.depends('amount_total')
    def _compute_one_eight(self):
        for record in self:
            record.one_eight = record.amount_total * 0.18


    @api.depends('amount_total', 'peaje_total', 'varios_total', 'stay_total')
    def _compute_gan(self):
        for record in self:
            total_peaje = record.peaje_total if record.peaje_total else 0.0
            total_varios = record.varios_total if record.varios_total else 0.0
            total_stay = record.stay_total if record.stay_total else 0.0
            
            record.total_gan = (record.amount_total * 0.18) + total_peaje + total_varios + total_stay


