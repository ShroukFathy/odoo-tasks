from odoo import fields, models

class ChangeState(models.TransientModel):
    _name = 'change.state'

    task_id = fields.Many2one('todo.task')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
    ],default='new')
    reason = fields.Char()

    def action_confirm(self):
        if self.task_id.status == 'closed':
            self.task_id.status= self.state
            self.task_id.create_todo_record_history('closed',self.state,reason=self.reason)

