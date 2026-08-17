from odoo import api, fields, models

class TodoHistory(models.Model):
    _name='todo.history'
    _description = 'Todo History'
    user_id=fields.Many2one('res.users')
    task_id=fields.Many2one('todo.task')
    old_state=fields.Char('Old State')
    new_state=fields.Char('New State')
    reason=fields.Char('Reason')
