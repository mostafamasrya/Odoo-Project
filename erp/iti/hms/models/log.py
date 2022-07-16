from odoo import models, fields, api


class LOghistory(models.Model):
    _name = "hms.log"
    description = fields.Text()
    patient_id = fields.Many2one('hms.patient')
