import base64
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from math import ceil

class SaleOrder(models.Model):
    _inherit = "sale.order"


    is_rental_order = fields.Boolean(
        string="Created In App Rental",
        compute='_compute_is_rental_order',
        store=True, precompute=True, readonly=False,
        default=lambda self: self.env.context.get('in_rental_app'))
    has_rented_products = fields.Boolean(compute='_compute_has_rented_products')
    rental_start_date = fields.Datetime(string="Rental Start Date", tracking=True)
    rental_return_date = fields.Datetime(string="Rental Return Date", tracking=True)
    duration_days = fields.Integer(
        string="Duration in days",
        compute='_compute_duration',
        help="The duration in days of the rental period.",
    )
    remaining_hours = fields.Integer(
        string="Remaining duration in hours",
        compute='_compute_duration',
        help="The leftover hours of the rental period.",
    )


    @api.depends('order_line.is_rental')
    def _compute_is_rental_order(self):
        for order in self:
            order.is_rental_order = order.is_rental_order or order.has_rented_products

    @api.depends('order_line.is_rental')
    def _compute_has_rented_products(self):
        for so in self:
            so.has_rented_products = any(line.is_rental for line in so.order_line)

    @api.depends('rental_start_date', 'rental_return_date')
    def _compute_duration(self):
        self.duration_days = 0
        self.remaining_hours = 0
        for order in self:
            if order.rental_start_date and order.rental_return_date:
                duration = order.rental_return_date - order.rental_start_date
                order.duration_days = duration.days
                order.remaining_hours = ceil(duration.seconds / 3600)
