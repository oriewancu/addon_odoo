# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        print("simpan master data Contacts dari modul gosantha_hospital")
        # do custom script here
        return res

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    patient_name = fields.Char(string='Nama Pasien')

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Master Pasien'
    _rec_name = 'patient_name'

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s %s' % (rec.name_seq, rec.patient_name)))
        return res

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

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    def action_send_card(self):
        print("sending email")
        template_id = self.env.ref('gosantha_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    patient_name = fields.Char(string='Nama', required=True, track_visibility='always')
    patient_age = fields.Integer(string='Umur', track_visibility='always')
    notes = fields.Text(string='Catatan')
    image = fields.Binary(string='Foto', attachment=True)
    name_seq = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jenis Kelamin', default='male')
    age_group = fields.Selection([
        ('dewasa', 'Dewasa'),
        ('anak', 'Anak')
    ], string='Grup Umur', compute='set_age_group', store=True)
    appointment_count = fields.Integer(string='Janji Bertemu', compute="get_appointment_count")
    active = fields.Boolean(string='Active', default=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Dokter')
    doctor_gender = fields.Selection([
        ('male', 'Laki-laki'),
        ('female', 'Perempuan')
    ], string='Jen. Kel. Dokter')
    email_id = fields.Char(
        string='Email',
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        return super(HospitalPatient, self).create(vals)