from odoo import models

class PatientCardXlsx(models.AbstractModel):
    _name = 'report.gosantha_hospital.report_patient_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patient):
        for lines in patient:
            print("lines", lines)
            boldvcenter = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
            vcenter = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
            sheet = workbook.add_worksheet('KP '+lines.patient_name)
            sheet.write(2, 2, 'Nama', boldvcenter)
            sheet.write(2, 3, lines.patient_name, vcenter)
            sheet.write(3, 2, 'Umur', boldvcenter)
            sheet.write(3, 3, lines.patient_age, vcenter)
            sheet.write(4, 2, 'Jen. Kel.', boldvcenter)
            sheet.write(4, 3, lines.gender, vcenter)