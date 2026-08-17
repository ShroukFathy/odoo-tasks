from odoo import fields, models, api
from odoo.exceptions import ValidationError

class TodoTask(models.Model):
    _name = 'todo.task'
    _rec_name = 'task_name'
    _inherit= ['mail.thread','mail.activity.mixin']
    task_name=fields.Char(string="Task Name",required=True)
    ref=fields.Char(string="Reference",default='New',readonly=True)
    assign_to=fields.Many2one('res.partner',string="Assign To")
    description=fields.Char(string="Description")
    due_date=fields.Datetime(string="Due Date")
    status=fields.Selection([
        ('new','New'),
        ('in_progress','In Progress'),
        ('completed','Completed'),
        ('closed', 'Closed'),

    ], default='new',string="Status", Tracking=True)
    total_time_spent=fields.Float(compute='_compute_total_time', string="Total Time Spent")
    timesheet_ids=fields.One2many('todo.timesheet','task_id',string="Timesheets")
    estimated_time=fields.Float(string="Estimated Time")
    active=fields.Boolean(default=True)
    is_late = fields.Boolean(compute='_compute_is_late', string="Late")

    def action_new(self):
        for rec in self:
            rec.create_todo_record_history(rec.status,'draft')
            rec.status = 'new'
    def action_inprogress(self):
        for rec in self:
            rec.create_todo_record_history(rec.status,'in_progress')
            rec.status = 'in_progress'

    def action_completed(self):
        for rec in self:
            rec.create_todo_record_history(rec.status,'completed')
            rec.status = 'completed'

    def action_closed(self):
        for rec in self:
            rec.create_todo_record_history(rec.status,'closed')
            rec.status = 'closed'

    @api.depends('due_date', 'status')
    def _compute_is_late(self):
        for rec in self:
            rec.is_late = bool(
                rec.due_date and rec.due_date < fields.Datetime.now() and rec.status not in ('completed', 'closed'))

    @api.depends('timesheet_ids.hours_spent')
    def _compute_total_time(self):
        for rec in self:
            rec.total_time_spent=sum(rec.timesheet_ids.mapped('hours_spent'))
    @api.constrains('total_time_spent','estimated_time')
    def _check_total_time(self):
        for rec in self:
            if rec.estimated_time < rec.total_time_spent:
                raise ValidationError("Total timesheet hours cannot exceed the estimated time")

    # def action_closed(self):
    #     for rec in self:
    #         rec.status = 'closed'

    def cron_check_late_tasks(self):
        late_tasks=self.search([('due_date','<',fields.Datetime.now()),
                                ('status','not in',['completed','closed']),])
        for rec in late_tasks:
            rec.message_post(body=f"Task '{rec.task_name}' is overdue!")
    # tare2a tanya -->
    # def _compute_total_time(self):
    #     for rec.self:
    #         total=0
    #         for line in rec.timesheet_ids:
    #             total+=line.hours_spent
    #     rec.total_time_spent=total
    @api.model
    def create(self,vals):
        res= super(TodoTask,self).create(vals)
        if res.ref=='New':
            res.ref = self.env['ir.sequence'].next_by_code('todo_seq')
        return res

    def create_todo_record_history(self,old_state,new_state,reason=False):
        for rec in self:
            rec.env['todo.history'].create({
                'user_id': rec.env.uid,
                'task_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
            })
    def action_open_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('todo.action_change_state_wizard')
        action['context']= {'default_task_id': self.id}
        return action




