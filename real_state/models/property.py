from odoo import api, fields, models
class Property(models.Model):
    _name = 'property'
    _description = 'is.realstate.property'

    name = fields.Char(required=True)
    bedrooms = fields.Integer(required=True)
    bathrooms = fields.Integer(required=True)
