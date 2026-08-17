from odoo import api, fields, models
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")
    vat = fields.Char(required=True)

    @api.constrains('email')
    def _check_email_not_patient(self):
        for partner in self:
            if partner.email:
                clash = self.env['hms.patient'].search([('email', '=', partner.email)], limit=1)
                if clash:
                    raise ValidationError(
                        "This email is already registered cant be used for a customer."
                    )

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                raise ValidationError("You cannot delete a customer that is conected to customer.")
        return super().unlink()