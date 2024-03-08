from odoo import models, fields


class StockOut(models.Model):
    _name = 'stock.out'
    _inherit = 'inventory.move'

    def get_quantity(self):
        return self.quantity
        