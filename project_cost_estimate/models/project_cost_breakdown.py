from odoo import fields, models, api
class ProjectCostBreakdown(models.Model):
    _name = 'project.cost.breakdown'

    name = fields.Char(string="Estimate")
    quantity=fields.Float(string='Quantity')
    unit_cost=fields.Float(string='Unit Cost')
    subtotal=fields.Float(compute='compute_subtotal',string='Sub Total',store=True)
    estimate_id=fields.Many2one(comodel_name='project.cost.estimate',string='Estimate')

    @api.depends('unit_cost','quantity')
    def compute_subtotal(self):
        for record in self:
            record.subtotal = record.unit_cost * record.quantity
