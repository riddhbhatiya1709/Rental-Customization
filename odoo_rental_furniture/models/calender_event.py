from odoo import api, fields, models


class Meeting(models.Model):
    _inherit = 'calendar.event'

    rental_product_template_id = fields.Many2one('product.template', string='Rental Product Template')
