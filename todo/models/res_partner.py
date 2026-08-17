from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    task_ids = fields.One2many('todo.task', 'assign_to', string="Assigned Tasks")