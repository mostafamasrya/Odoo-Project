from odoo import models, fields, api
import re
from odoo.exceptions import ValidationError
from datetime import date


class PatientHsp(models.Model):
    _name = "hms.patient"
    firstname = fields.Char(required=True)
    lastname = fields.Char(required=True)
    b_date = fields.Date()
    history = fields.Html()
    CR_ration = fields.Float()
    BloodType = fields.Selection([('a', 'A+'), ('b', 'B+'), ('o', 'O+')])
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age = fields.Integer(compute='age_calc')
    state = fields.Selection(
        [('undetermined', 'Undetermined'), ('good', 'Good'), ('fair', 'Fair'), ('serious', 'Serious')],
        default='undetermined')
    departmentNo = fields.Many2one('hms.department')
    doctor = fields.Many2many('hms.doctor')
    dep_capacity = fields.Integer(related='departmentNo.capacity')
    log_ids=fields.One2many('hms.log','patient_id')
    email=fields.Char()



    _sql_constraints = [('unique_const_email','UNIQUE(email)','email must be unique')]

    @api.constrains('email')
    def _onchange_email(self):
        if self.email:

            myemail=re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',self.email)
            if not myemail:
                raise ValidationError("email is not valid")


    @api.depends('b_date')
    def age_calc(self):
        print("calc.............")
        for rec in self:
            if rec.b_date:
                rec.age=date.today().year-rec.b_date.year
            else:
                rec.age=0


    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {'warning': {'title': 'changing pcr selection',
                                'message': 'you have age less then 30 so pcr is selected'}}
        else:
            self.pcr = False

    def go_to_undetermined(self):
        self.state = "undetermined"

        self.env['hms.log'].create({'description':"history of patient is undtermined",'patient_id' : self.id})

    def go_to_good(self):
        self.state = "good"
        self.env['hms.log'].create({'description':"history of patient is good",'patient_id' : self.id})


    def go_to_fair(self):
        self.state = "fair"
        self.env['hms.log'].create({'description':"history of patient is fair",'patient_id' : self.id})


    def go_to_serious(self):
        self.state = "serious"
        self.env['hms.log'].create({'description':"history of patient is serious",'patient_id' : self.id})

