from odoo import fields, models, api

class ResCompany(models.Model):
    _inherit = 'res.company'
    cost_estimate_seq=fields.Char(string='Cost Estimate sequence')
