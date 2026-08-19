from odoo import api, fields, models

class ProjectCostEstimateHistory(models.Model):
    _name='project.cost.estimate.history'
    _description = 'estimate History'
    user_id=fields.Many2one('res.users')
    estimate_id=fields.Many2one('project.cost.estimate')
    old_state=fields.Char('Old State')
    new_state=fields.Char('New State')
    reason=fields.Char('Reason')
