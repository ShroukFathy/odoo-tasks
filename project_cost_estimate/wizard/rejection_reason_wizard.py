from odoo import fields, models

class RejectionReason(models.TransientModel):
    _name = 'rejection.reason'

    estimate_id = fields.Many2one('project.cost.estimate',required=True)
    reason = fields.Char(string="Reason",required=True)

    def action_confirm(self):
        if self.estimate_id.state == 'submitted':
            old_state = self.estimate_id.state
            self.estimate_id.state = 'rejected'
            self.estimate_id.create_cost_estimate_record_history(old_state, 'rejected', reason=self.reason)