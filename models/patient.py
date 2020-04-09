# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Nama Pasien')

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Master Pasien'
    _rec_name = 'patient_name'

    @api.constrains('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_('Umur harus lebih besar dari 5.'))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'anak'
                else:
                    rec.age_group = 'dewasa'
    
    @api.multi
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    patient_name = fields.Char(string='Nama', required=True, track_visibility='always')
    patient_age = fields.Integer(string='Umur', track_visibility='always')
    notes = fields.Text(string='Catatan')
    image = fields.Binary(string='Foto', attachment=True)
    name_seq = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('New'))
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin', default='male')
    age_group = fields.Selection([
        ('dewasa', 'Dewasa'),
        ('anak', 'Anak')
    ], string='Grup Umur', compute='set_age_group', store=True)
    appointment_count = fields.Integer(string='Janji Bertemu', compute="get_appointment_count")

    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or ('New')
        return super(HospitalPatient, self).create(vals)