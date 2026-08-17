from odoo import fields, models, api
from odoo.exceptions import UserError

class ProjectCostEstimate(models.Model):
    _name = 'project.cost.estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char(string="name")
    project_id=fields.Many2one('project.project',required=True)
    breakdown_ids= fields.One2many('project.cost.breakdown','estimate_id', string="Line cost")
    estimated_total_cost= fields.Float(compute='compute_estimated_total_cost',string="Estimated Total Cost", store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='draft', string="Status", tracking=True)

    @api.depends('breakdown_ids.subtotal')
    def compute_estimated_total_cost(self): 
         for rec in self:
             total=0
             for line in rec.breakdown_ids:
                 total+= line.subtotal
             rec.estimated_total_cost = total

    def action_submit(self):
        for rec in self:
            if not self.env.user.has_group('project_cost_estimate.group_project_cost_admin'):
                raise UserError("Only project asmins can submit a cost estimate.")
            rec.state = 'submitted'

    def action_approve(self):
        for rec in self:
            if not self.env.user.has_group('project_cost_estimate.group_project_super_admin'):
                raise UserError("You are not allowed to approve cost estimates.")
            rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            if not self.env.user.has_group('project_cost_estimate.group_project_super_admin'):
                raise UserError("You are not allowed to rejevt cost estimates.")
            rec.state = 'rejected'
    def write(self,vals):
        res=super().write(vals)
        if 'state' in vals and vals['state'] in('approved', 'rejected'):
            for rec in self:
                rec.send_state_email(vals['state'])
        return res
    def send_state_email(self,state):
        self.ensure_one()
        self.message_post(
            partner_ids=[self.create_uid.partner_id.id],
            subject=f"Cost Estimate: {state.capitalize()}",
            body=f"Your cost estimate {self.name} has been {state}.",
        )










