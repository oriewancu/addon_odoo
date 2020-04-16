# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Janji Bertemu'
    _order = "appointment_date desc, name asc"

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        return super(HospitalAppointment, self).create(vals)

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, 
                        index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Pasien', required=True)
    patient_age = fields.Integer(string='Umur', related="patient_id.patient_age")
    notes = fields.Text(string='Kode Registrasi')
    doctor_note = fields.Text(string='Catatan')
    pharmacy_note = fields.Text(string='Catatan')
    appointment_date = fields.Date(string='Tanggal', required=True)
    state = fields.Selection([
        ('draft', 'Draf'),
        ('confirm', 'Konfirmasi'),
        ('done', 'Selesai'),
        ('cancel', 'Dibatalkan'),
    ], string='Status', readOnly=True, default='draft')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string="Detail Obat")

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Detail Obat'
    
    product_id = fields.Many2one('product.product', string='Obat')
    product_qty = fields.Integer(string='Jumlah')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
