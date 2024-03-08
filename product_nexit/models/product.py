from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = 'product.inventory'
    _description = 'Product in inventory'

    name = fields.Char(string='Name of product', required=True)
    quantity_on_hand = fields.Integer(string='Quantity on hand', default=0,compute='_compute_quantity_on_hand')
    inventory_cost = fields.Integer(string='Inventory Cost', compute='_compute_cost_price')
    cost_price = fields.Float(string='Price of product', )
    in_moves_ids = fields.One2many('stock.in', 'product_id', string='In Moves')
    out_moves_ids = fields.One2many('stock.out', 'product_id', string='Out Moves')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Product name must be unique.'),
    ]

    @api.constrains('cost_price')
    def _check_cost_price(self):
        for res in self: 
            if res.cost_price <= 0:
                raise ValidationError('El precio del producto no puede ser menor o igual que 0')


    @api.depends('in_moves_ids','out_moves_ids')
    def _compute_quantity_on_hand(self):
        for rec in self:
            rec.quantity_on_hand = rec.in_moves_ids.quantity - rec.out_moves_ids.quantity


    @api.depends('cost_price','quantity_on_hand')
    def _compute_cost_price(self):
        for rec in self: 
            rec.inventory_cost = rec.quantity_on_hand * rec.cost_price
        
    
    

    # @api.onchange('in_moves_ids','out_moves_ids')
    # def onchange_inventory(self):
        
    #     self.quantity_on_hand = self.in_moves_ids.quantity - self.out_moves_ids.quantity
    #     self.inventory_cost = self.quantity_on_hand * self.cost_price
