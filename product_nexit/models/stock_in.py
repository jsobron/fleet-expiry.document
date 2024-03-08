from odoo import models, fields


class StockIn(models.Model):
    _name = 'stock.in'
    _inherit = 'inventory.move'
    
    def get_quantity(self):
        return self.quantity
