from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _rec_name = 'name'
    name = fields.Char(string="Full Name", compute='_compute_name', store=True)
    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)

    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ])

    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age', store=True, string="Age")
    email = fields.Char(string="Email", readonly=True)
    address = fields.Char()
    history = fields.Html()
    cr_ratio = fields.Float()
    pcr = fields.Boolean()
    image = fields.Image()

    doctor_id = fields.Many2many('hms.doctors', string='Doctor')
    department_id = fields.Many2one(
        'hms.department', string="Department",
        domain="[('state', '=', 'open')]"
    )
    department_capacity = fields.Integer(
        related='department_id.capacity', string='Department Capacity', readonly=True
    )

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined')

    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Log History")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name or ''} {rec.last_name or ''}".strip()

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0

    @api.onchange('age')
    def _onchange_age(self):
        if self.age is not None and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Auto-checked",
                    'message': "PCR has been automatically checked because the patient is under 30.",
                }
            }

    # @api.constrains('department_id')
    # def _check_department_open(self):
    #     for patient in self:
    #         if patient.department_id and patient.department_id.state == 'closed':
    #             raise ValidationError("You can't assign a patient to a closed department.")

    @api.onchange('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.model
    def create(self, vals):
        if vals.get('first_name') and vals.get('last_name'):
            vals['email'] = f"{vals['first_name'][0]}{vals['last_name']}@gmail.com".lower()
            searched_list = self.search([('email', '=', vals['email'])])
            if len(searched_list) > 0:
                raise UserError("The email already exists")
        return super().create(vals)

    def write(self, vals):
        if 'state' in vals:
            state_labels = dict(self._fields['state'].selection)
            for patient in self:
                if vals['state'] != patient.state:
                    self.env['hms.patient.log'].create([{
                        'patient_id': patient.id,
                        'description': f"State changed to {state_labels.get(vals['state'])}",
                    }])

        return super().write(vals)
    def move_to_good(self):
        self.state='good'

    def move_to_fair(self):
        self.state='fair'

    def move_to_serious(self):
        self.state='serious'