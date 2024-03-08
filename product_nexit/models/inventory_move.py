from odoo import models, fields


class InventoryMoveAbstract(models.AbstractModel):
    _name = 'inventory.move'
    _description = 'Inventory Move'

    product_id = fields.Many2one('product.inventory', string='Product')
    quantity = fields.Integer(string='Quantity in Move')
    move_date = fields.Date(string='Move Date', default=fields.Date.today)

    def get_quantity(self):
        return self.quantity
