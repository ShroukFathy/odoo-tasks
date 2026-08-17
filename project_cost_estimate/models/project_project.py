from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    cost_estimate_ids = fields.One2many('project.cost.estimate', 'project_id', string="Cost Estimates")
    cost_estimate_count = fields.Integer(string="Cost Estimate Count", compute='_compute_cost_estimate_count')

    def _compute_cost_estimate_count(self):
        for project in self:
            project.cost_estimate_count = len(project.cost_estimate_ids)

    def action_view_cost_estimates(self):
        self.ensure_one()
        return {
            'name': 'Cost Estimates',
            'type': 'ir.actions.act_window',
            'res_model': 'project.cost.estimate',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }