from odoo import models

class ReportBookDayrXlsx(ReportXlsx):
    _name = "report.book.day.xls"
    _inherit = "report.report_xlsx_abstract"

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, obj.name, bold)


PartnerXlsx('report.res.partner.xlsx',
            'res.partner')