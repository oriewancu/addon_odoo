from odoo import fields, models, api


class CreateAppointment (models.TransientModel):
    _name = 'create.appointment'
    _description = 'Wizard Membuat Janji Bertemu'

    patient_id = fields.Many2one('hospital.patient', string="Pasien")
    appointment_date = fields.Date(string="Tanggal")
    
    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date
        }
        self.env['hospital.appointment'].create(vals)

