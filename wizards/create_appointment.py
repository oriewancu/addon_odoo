from odoo import fields, models, api


class CreateAppointment (models.Model):
    _name = 'create.appointment'
    _description = 'Wizard Membuat Janji Bertemu'

    patient_id = fields.Many2one('hospital.patient', string="Pasien")
    appointment_date = fields.Date(string="Tanggal")
    


