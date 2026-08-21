from odoo import fields,models
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    cost_estimate_seq=fields.Char(string="Cost Estimate", related='company_id.cost_estimate_seq',readonly=False)

    def write(self,vals):
        res=super(ResConfigSettings,self).write(vals)
        if 'cost_estimate_seq' in vals:
            self.env.company.write({'cost_estimate_seq' : vals.get('cost_estimate_seq')})
            return res

