from odoo import models , fields

class DoctorHsp(models.Model):
    _name='hms.doctor'
    firstname=fields.Char()
    lastname=fields.Char()
    image=fields.Image()
