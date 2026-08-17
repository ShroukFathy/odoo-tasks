from odoo import fields, models
class HMSDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'HMS Doctors'
    name=fields.Char(string='Name')
    image = fields.Image(string='Image')
    department_id=fields.Many2one(comodel_name='hms.department')
    patient_id=fields.Many2many('hms.patient',string='Patient')
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender')
    date_of_birth = fields.Date(string='Date of Birth')
    phone=fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    license_number=fields.Char(string='Licence Number')
    department = fields.Char(string='Department')

