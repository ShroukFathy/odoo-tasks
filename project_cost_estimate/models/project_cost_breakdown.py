from odoo import fields, models, api
from odoo.exceptions import ValidationError
class ProjectCostBreakdown(models.Model):
    _name = 'project.cost.breakdown'

    # name = fields.Char(string="Estimate")
    product_id = fields.Many2one(comodel_name='product.product', string="Estimate", required=True)
    quantity=fields.Float(string='Quantity')
    unit_cost=fields.Float(string='Unit Cost')
    subtotal=fields.Float(compute='compute_subtotal',string='Sub Total',store=True)
    estimate_id=fields.Many2one(comodel_name='project.cost.estimate',string='Estimate')



    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.unit_cost=self.product_id.standard_price

    @api.depends('unit_cost','quantity')
    def compute_subtotal(self):
        for record in self:
            record.subtotal = record.unit_cost * record.quantity

    @api.constrains('unit_cost','quantity')
    def check_not_negative(self):
        for rec in self:
            if rec.quantity<1 :
                raise ValidationError("Quantity cannot be less than One.")
            if rec.unit_cost<0:
                raise ValidationError("Unit cost cannot be negative.")