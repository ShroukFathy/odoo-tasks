from odoo import api, fields, models
class HMSDepartment(models.Model):
    _name = 'hms.department'
    _description = 'HMS Department'
    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    doctor_id=fields.One2many('hms.doctors','department_id',string='Doctor')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string="Status", default='open', required=True)
