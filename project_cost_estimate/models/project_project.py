from odoo import fields, models, api

class ProjectProject(models.Model):
    _inherit = 'project.project'

    cost_estimate_ids = fields.One2many('project.cost.estimate', 'project_id', string="Cost Estimates")
    cost_estimate_count = fields.Integer(string="Cost Estimate Count", compute='_compute_cost_estimate_count')
    latest_cost_estimate = fields.Float(string="Latest Cost Estimate", compute='_compute_latest_cost_estimate')
    latest_cost_estimate_state = fields.Char(string="Latest Estimate state", compute='_compute_latest_cost_estimate_state')

    @api.depends('cost_estimate_ids.create_date', 'cost_estimate_ids.estimated_total_cost', 'cost_estimate_ids.state')
    def _compute_latest_cost_estimate(self):
        for project in self:
            latest = project.cost_estimate_ids.sorted('create_date', reverse=True)[:1]
            if latest:
                project.latest_cost_estimate = latest.estimated_total_cost
                project.latest_cost_estimate_state = latest.state
            else:
                project.latest_cost_estimate = 0.0
                project.latest_cost_estimate_state = False


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