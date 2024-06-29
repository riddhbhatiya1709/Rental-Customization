# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rent_ok = fields.Boolean(
        string="Can be Rented",
        help="Allow renting of this product.")

    rent_price_on_day = fields.Float(
        string="Rent Price (Per Day)",
        help="Rent price for single day."
    )

    qty_in_rent = fields.Float("Quantity currently in rent", compute='_get_qty_in_rent')
    display_price = fields.Char(
        string="Rental price",
        compute='_compute_display_price',
        help="First rental pricing of the product",
    )
