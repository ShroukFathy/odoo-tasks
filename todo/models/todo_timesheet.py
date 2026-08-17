from odoo import fields, models

class TodoTimesheet(models.Model):
    _name ='todo.timesheet'

    task_id=fields.Many2one('todo.task',string='Task',required=True)
    description=fields.Char(string='Description',required=True)
    hours_spent=fields.Float(string='Hours spent',required=True)
    date=fields.Date(string='Date',required=True)
    user_id=fields.Many2one('res.users',string='User',required=True)


